# app.py
from flask import Flask, request, jsonify
from reranker import retrieve_contexts
import os

app = Flask(__name__)

# Define a confidence threshold for abstention
# (Note: This is a placeholder value and should be tuned)
CONFIDENCE_THRESHOLD = 0.5

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('q')
    k = data.get('k', 5)
    mode = data.get('mode', 'reranker')

    if not query:
        return jsonify({"error": "Query 'q' is required"}), 400

    # Retrieve contexts from reranker.py
    retrieved_contexts, reranker_used = retrieve_contexts(query, k, mode)

    answer = None
    if not retrieved_contexts:
        answer = "I am sorry, but I could not find any relevant information."
    else:
        top_chunk = retrieved_contexts[0]
        
        # Determine the correct score based on the mode
        if mode == 'baseline':
            score = 1 - top_chunk.get('score', 1.0) # We need to convert distance to similarity
            if score < CONFIDENCE_THRESHOLD:
                answer = "I am sorry, but the most relevant information found has a low confidence score."
            else:
                answer = top_chunk['text']

        elif mode == 'reranker':
            score = top_chunk.get('combined_score', 0.0)
            if score < CONFIDENCE_THRESHOLD:
                answer = "I am sorry, but the most relevant information found has a low confidence score."
            else:
                answer = top_chunk['text']
        else:
            answer = "I am sorry, but an invalid mode was selected."

    return jsonify({
        "answer": answer,
        "contexts": retrieved_contexts,
        "reranker_used": reranker_used
    })

if __name__ == '__main__':
    app.run(debug=True)