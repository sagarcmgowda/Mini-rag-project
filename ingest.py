# ingest.py
import json
import sqlite3
import zipfile
import os
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# --- Configuration ---
PDF_ZIP_FILE = 'industrial-safety-pdfs.zip'
SOURCES_JSON_FILE = 'sources.json'
PDFS_DIR = 'pdfs'
DATA_DIR = 'data'
DB_FILE = os.path.join(DATA_DIR, 'chunks.db')
FAISS_INDEX_FILE = os.path.join(DATA_DIR, 'faiss_index.bin')
CHUNK_IDS_FILE = os.path.join(DATA_DIR, 'chunk_ids.npy')

# Ensure directories exist
os.makedirs(PDFS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# --- Step 1: Unzip PDFs and load sources ---
print("Step 1: Unzipping PDFs and loading sources.json...")
try:
    with zipfile.ZipFile(PDF_ZIP_FILE, 'r') as z:
        z.extractall(PDFS_DIR)
        extracted_files = {os.path.basename(f) for f in z.namelist()}
except FileNotFoundError:
    print(f"Error: {PDF_ZIP_FILE} not found. Please place the file in the project root.")
    exit()

with open(SOURCES_JSON_FILE, 'r') as f:
    sources_data = json.load(f)

# --- Step 2: Ingest and chunk documents into SQLite ---
print("Step 2: Ingesting documents and chunking text...")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Drop existing table to ensure a fresh start
cursor.execute('DROP TABLE IF EXISTS chunks')
cursor.execute('''
    CREATE TABLE chunks (
        id INTEGER PRIMARY key,
        text TEXT NOT NULL,
        source_title TEXT,
        source_url TEXT,
        page_number INTEGER
    );
''')

chunks_list = []
chunk_id = 0
for source in sources_data:
    try:
        # A more robust way to get the filename from the URL, but the ZIP content is the source of truth
        filename_from_url = os.path.basename(source['url'].split('?')[0])
        pdf_path = None
        
        # Match the filename in the sources.json to the list of extracted files
        for f in extracted_files:
            if filename_from_url in f or source['title'].split(' ')[0] in f:
                pdf_path = os.path.join(PDFS_DIR, f)
                break
        
        if not pdf_path or not os.path.exists(pdf_path):
             print(f"Warning: PDF file for '{source['title']}' not found. Skipping.")
             continue

        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing '{source['title']}' from {os.path.basename(pdf_path)}...")
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    paragraphs = text.split('\n\n')
                    for para in paragraphs:
                        clean_para = ' '.join(para.strip().split())
                        if len(clean_para) > 100:
                            chunks_list.append({
                                'id': chunk_id,
                                'text': clean_para,
                                'source_title': source['title'],
                                'source_url': source['url'],
                                'page_number': page_num + 1
                            })
                            cursor.execute("INSERT INTO chunks VALUES (?, ?, ?, ?, ?)",
                                           (chunk_id, clean_para, source['title'], source['url'], page_num + 1))
                            chunk_id += 1
    except Exception as e:
        print(f"Error processing {source['title']}: {e}")

conn.commit()
conn.close()
print(f"Ingestion complete. {len(chunks_list)} chunks created.")

# --- Step 3: Generate embeddings and build FAISS index ---
print("\nStep 3: Generating embeddings and building FAISS index...")
if not chunks_list:
    print("No chunks were created. Aborting embedding and indexing.")
else:
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        texts = [chunk['text'] for chunk in chunks_list]
        embeddings = model.encode(texts, convert_to_tensor=False, show_progress_bar=True)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings, dtype='float32'))

        # Save the FAISS index and the chunk ID mapping
        faiss.write_index(index, FAISS_INDEX_FILE)
        chunk_ids = np.array([chunk['id'] for chunk in chunks_list])
        np.save(CHUNK_IDS_FILE, chunk_ids)

        print("Embeddings and index saved successfully.")

    except Exception as e:
        print(f"Error during embedding or indexing: {e}")

        