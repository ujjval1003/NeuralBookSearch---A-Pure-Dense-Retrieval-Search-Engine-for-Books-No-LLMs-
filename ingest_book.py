# Copyright 2026 Ujjval Patel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import psycopg2
from fastembed import TextEmbedding
from extract_book import extract_pdf
from chunk_book import chunk_text
from sentence_split import split_sentences
from tqdm import tqdm

DB_CONFIG = {
    "host": "db.YOUR_DB_NAME.supabase.co",
    "database": "postgres",
    "user": "postgres",
    "password": "YOUR_PASSWORD",
    "port": 5432,
}
embedder = TextEmbedding("BAAI/bge-small-en-v1.5", providers=["CUDAExecutionProvider"]) # Remove providers=["CUDAExecutionProvider"] if you don't have NVIDIA GPU

def ingest(pdf_path):
    print("Opening PDF...")
    pages = extract_pdf(pdf_path)
    print("Chunking book...")
    chunks = chunk_text(pages)
    print("Total chunks created:", len(chunks))
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    print("Generating embeddings and uploading to pgvector...")
    for page, content in tqdm(chunks):
        sentences = split_sentences(content)
        for sent in sentences:
            emb = list(embedder.embed([f"passage: {sent}"]))[0].tolist()
            cur.execute(
                """
                INSERT INTO book_chunks (content, page_number, embedding)
                VALUES (%s, %s, %s)
                """,
                (sent, page, emb)
            )
    conn.commit()
    conn.close()
    print("\nBOOK INDEXING COMPLETE")

if __name__ == "__main__":
    ingest("../book1.pdf")