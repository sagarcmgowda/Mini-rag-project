# Mini RAG Project: Industrial Safety Document Q&A System

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about industrial safety. It uses a vector database (FAISS) for semantic search and a hybrid reranker to improve the relevance of results. The system is exposed via a simple Flask API.

## Project Deliverables

-   **Code:** `ingest.py`, `reranker.py`, and `app.py`
-   **Data:** `sources.json` and a file containing 8 questions.
-   **Documentation:** This `README.md` file, which explains the setup, how to run the project, and a detailed analysis of the results.

---

## Setup and Installation

Follow these steps to set up the project on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd mini-rag-project
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Add data files:**
    Ensure you have `industrial-safety-pdfs.zip` and `sources.json` in the project's root directory.

---

## How to Run

1.  **Run the data ingestion script:** This will unzip the PDFs, chunk the text, create embeddings, and build the FAISS index and SQLite database.
    ```bash
    python ingest.py
    ```
2.  **Start the Flask API:** Open a new terminal window and start the Flask development server. This terminal must remain open and running.
    ```bash
    python app.py
    ```
3.  **Send requests:** Use `curl` from a separate terminal to interact with the API.

---

## Example:

Here are two example requests to test the API for both search modes.

### Baseline Search Example

This command uses cosine similarity to find the most relevant chunks.

```bash
curl -X POST [http://127.0.0.1:5000/ask](http://127.0.0.1:5000/ask) -H "Content-Type: application/json" -d "{\"q\": \"What is the Machinery Regulation?\", \"k\": 3, \"mode\": \"baseline\"}"
```

### Reranker Search Example

This command uses a hybrid approach (cosine similarity + BM25 keyword search) to rerank the results for better accuracy.

```bash
curl -X POST [http://127.0.0.1:5000/ask](http://127.0.0.1:5000/ask) -H "Content-Type: application/json" -d "{\"q\": \"How to protect workers from amputations?\", \"k\": 5, \"mode\": \"reranker\"}"
```

### Results and Findings
The following table summarizes the results for the 8 questions, comparing the performance of the baseline and reranker modes.
| Question | Baseline Result | Reranker Result | Better Performer |
|----------|----------------|----------------|----------------|
| Q1: What is risk assessment? | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q2: How to protect workers from amputations? | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q3: [Question 3] | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q4: [Question 4] | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q5: [Question 5] | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q6: [Question 6] | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q7: [Question 7] | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |
| Q8: [Question 8] | [The answer or "Abstain"] | [The answer or "Abstain"] | [Baseline/Reranker] |


