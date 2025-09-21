# reranker.py
import sqlite3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import os

# --- Configuration ---
DATA_DIR = 'data'
DB_FILE = os.path.join(DATA_DIR, 'chunks.db')
FAISS_INDEX_FILE = os.path.join(DATA_DIR, 'faiss_index.bin')
CHUNK_IDS_FILE = os.path.join(DATA_DIR, 'chunk_ids.npy')

# --- Load models and index (once) ---
model = SentenceTransformer('all-MiniLM-L6-v2')
faiss_index = faiss.read_index(FAISS_INDEX_FILE)
chunk_ids_map = np.load(CHUNK_IDS_FILE)

# --- Retrieval and Reranking Logic ---
def retrieve_contexts(query: str, k: int, mode: str):
    # Generate embedding for the query
    query_embedding = model.encode([query], convert_to_tensor=False)
    
    # Perform vector similarity search
    # We retrieve more results initially to give the reranker more options
    search_k = k * 2 if mode == 'reranker' else k
    D, I = faiss_index.search(np.array(query_embedding, dtype='float32'), search_k)
    
    retrieved_chunk_indices = I[0]
    
    # --- Now, get the full chunks from the database ---
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    contexts = []
    
    for i, faiss_id in enumerate(retrieved_chunk_indices):
        chunk_db_id = chunk_ids_map[faiss_id]
        cursor.execute("SELECT * FROM chunks WHERE id = ?", (int(chunk_db_id),))
        row = cursor.fetchone()
        if row:
            contexts.append({
                "id": row[0],
                "text": row[1],
                "source_title": row[2],
                "source_url": row[3],
                "page_number": row[4],
                "score": float(D[0][i])
            })
    
    conn.close()

    # --- Reranking with BM25 (if mode is 'reranker') ---
    if mode == 'reranker' and len(contexts) > 1:
        corpus = [ctx['text'] for ctx in contexts]
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = query.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        
        # Normalize and combine scores
        combined_scores = []
        for i, ctx in enumerate(contexts):
            # Normalizing the FAISS score (lower is better, so we use 1 - normalized_score)
            max_faiss_dist = max(ctx['score'] for ctx in contexts)
            faiss_score_normalized = 1 - (ctx['score'] / max_faiss_dist) if max_faiss_dist > 0 else 0
            
            # Normalizing the BM25 score (higher is better)
            max_bm25_score = max(doc_scores)
            bm25_score_normalized = doc_scores[i] / max_bm25_score if max_bm25_score > 0 else 0
            
            combined_score = 0.5 * faiss_score_normalized + 0.5 * bm25_score_normalized
            ctx['combined_score'] = combined_score
        
        contexts.sort(key=lambda x: x['combined_score'], reverse=True)
        return contexts[:k], True # Return the top k reranked contexts and True
    
    return contexts[:k], False # For baseline, return the top k contexts and False