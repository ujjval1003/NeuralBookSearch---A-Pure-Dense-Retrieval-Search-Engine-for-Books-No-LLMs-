# NeuralBookSearch

### A Pure Dense Retrieval Search Engine for Large Books (No LLMs)

NeuralBookSearch is a semantic search engine that can understand and answer questions directly from large textbooks or novels **without using any Large Language Model (LLM)**.

Instead of generating answers, the system retrieves the most relevant knowledge passages using **dense embeddings (BGE-small)**, multi-query retrieval, hybrid ranking, and multi-hop reasoning.

The project demonstrates how modern AI retrieval systems work internally — similar to the retrieval layer used in RAG systems and search engines — but implemented entirely from scratch in Python.

---

## 🚀 What This Project Does

The system allows you to:

* Index a 500–1000+ page book
* Convert the entire book into semantic vectors
* Ask natural language questions
* Retrieve correct passages from the book
* Compare two concepts (example: *Greedy vs Uniform Cost Search*)
* Perform multi-step retrieval reasoning

**Important:**
This is NOT a chatbot.
This is a **neural knowledge retrieval engine**.

It does not generate answers — it finds the exact knowledge inside the book.

---

## 🧠 How It Works (Pipeline)

```
PDF Book
   ↓
Text Extraction
   ↓
Cleaning & Chunking
   ↓
Sentence Segmentation
   ↓
Embedding (BGE-small)
   ↓
Vector Database (pgvector)
   ↓
Dense Retrieval
   ↓
Reranking + Hybrid Scoring
   ↓
Multi-hop Reasoning
   ↓
Relevant Knowledge Passages
```

---

## 🔬 Core Techniques Used

* Dense Embeddings (BAAI/bge-small-en-v1.5)
* Vector Databases (PostgreSQL + pgvector)
* Semantic Search
* Multi-Query Retrieval
* Hybrid Retrieval (Neural + Keyword)
* Two-Stage Reranking
* Multi-Hop Retrieval
* Concept Comparison Engine

---

## 📁 Project Structure

### Document Processing

| File                | Purpose                                    |
| ------------------- | ------------------------------------------ |
| `extract_book.py`   | Extracts raw text from PDF pages           |
| `chunk_book.py`     | Cleans text and creates overlapping chunks |
| `sentence_split.py` | Splits chunks into meaningful sentences    |

---

### Indexing (Vectorization)

| File                   | Purpose                                                        |
| ---------------------- | -------------------------------------------------------------- |
| `ingest_book.py`       | Converts sentences into embeddings and stores them in pgvector |
| `build_local_index.py` | Creates a local neural index for reranking                     |

---

### Retrieval Engine

| File                | Purpose                                          |
| ------------------- | ------------------------------------------------ |
| `retrieval_core.py` | Multi-query dense retrieval from vector database |
| `rerank.py`         | Second-stage reranking using cosine similarity   |
| `hybrid_score.py`   | Combines keyword match + neural similarity       |
| `query_expand.py`   | Expands queries into multiple semantic forms     |

---

### Intelligence Layer

| File                | Purpose                                                   |
| ------------------- | --------------------------------------------------------- |
| `compare_engine.py` | Searches and compares two concepts                        |
| `multi_hop.py`      | Performs reasoning by retrieving new queries from results |
| `query_type.py`     | Detects comparison queries                                |
| `answer_builder.py` | Formats explanation output                                |
| `search_book.py`    | Main program (user interface & orchestration)             |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/NeuralBookSearch.git
cd NeuralBookSearch
```

---

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup PostgreSQL + pgvector

Install PostgreSQL (v15+ recommended)

Then inside PostgreSQL:

```sql
CREATE EXTENSION vector;

CREATE TABLE book_chunks (
    id SERIAL PRIMARY KEY,
    content TEXT,
    page_number INT,
    embedding VECTOR(384)
);
```

---

### 4️⃣ Add Your Book

Place your PDF here:

```
/Search Engin/book1.pdf
```

---

## ▶️ How To Run

### Step 1 — Index the Book

```bash
python ingest_book.py
```

(This converts the entire book into semantic vectors)

---

### Step 2 — Build Reranking Index

```bash
python build_local_index.py
```

---

### Step 3 — Start Search Engine

```bash
python search_book.py
```

Now ask questions:

Example:

```
what is rational agent
why A* optimal
difference between greedy search and uniform cost search
what is markov decision process
```

---

## 🧪 Example Queries

* define admissible heuristic
* explain forward chaining
* compare greedy search and a star search
* what is inference
* difference supervised and reinforcement learning

---

## 🎯 Goals of the Project

This project was created to:

* Understand how search engines retrieve knowledge
* Push small embedding models to their limits
* Study retrieval accuracy without using LLMs
* Explore dense retrieval research concepts

---

## ❗ What This Project Is NOT

* Not a chatbot
* Not a RAG system
* Not GPT-like
* No text generation

It is a **pure retrieval system**.

---

## 👤 Author

Ujjval Patel

---

## ⭐ If you found this interesting

Star the repository and experiment with your own books!
