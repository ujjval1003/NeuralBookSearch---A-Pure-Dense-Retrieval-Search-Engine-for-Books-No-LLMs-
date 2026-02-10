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
from query_expand import expand_query
from rerank import rerank
from hybrid_score import keyword_score
from multi_hop import multi_hop_queries
from compare_engine import compare
from query_type import is_comparison
from answer_builder import build_comparison_answer

DB_CONFIG = {
    "host": "db.YOUR_DB_NAME.supabase.co",
    "database": "postgres",
    "user": "postgres",
    "password": "YOUR_PASSWORD",
    "port": 5432,
}
embedder = TextEmbedding("BAAI/bge-small-en-v1.5", providers=["CUDAExecutionProvider"]) # Remove providers=["CUDAExecutionProvider"] if you don't have NVIDIA GPU

def retrieve_candidates(query, per_query_k=120):
    """
    Multi-query dense retrieval
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    expanded_queries = expand_query(query)
    candidates = {}
    query_inputs = [f"query: {q}" for q in expanded_queries]
    query_embeddings = list(embedder.embed(query_inputs))
    for q_emb in query_embeddings:
        q_emb = q_emb.tolist()
        cur.execute(
            """
            SELECT content, page_number,
                   1 - (embedding <=> %s::vector) AS score
            FROM book_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (q_emb, q_emb, per_query_k)
        )
        for content, page, score in cur.fetchall():
            key = (content, page)
            candidates[key] = max(score, candidates.get(key, 0))
    conn.close()
    return list(candidates.keys())

def final_rank(query, candidates):
    """
    Neural rerank + keyword hybrid
    """
    neural_ranked = rerank(query, candidates)
    final = []
    for text, page, neural_score in neural_ranked:
        kw_score = keyword_score(query, text)
        score = 0.75 * neural_score + 0.25 * kw_score
        final.append((text, page, score))
    max_score = max(s for _,_,s in final)
    min_score = min(s for _,_,s in final)
    normalized = []
    for text,page,score in final:
        if max_score != min_score:
            score = (score - min_score)/(max_score-min_score)
        normalized.append((text,page,score))
    return sorted(normalized, key=lambda x:x[2], reverse=True)

if __name__ == "__main__":
    print("\nNeural Book Search (type exit to quit)\n")
    while True:
        q = input("Question: ")
        if q.lower() == "exit":
            break
        if is_comparison(q):
            comparison = compare(q)
            print("\n=== COMPARISON MODE ===\n")
            if not comparison:
                print("Could not identify two clear concepts.\n")
                continue
            for concept, passages in comparison.items():
                print(f"\n### {concept.upper()} ###\n")
                for text, page, score in passages[:4]:
                    print(f"(page {page}) {text[:350]}\n")
            summary = build_comparison_answer(comparison)
            if summary:
                print(summary)
            print("\n" + "="*70 + "\n")
            continue
        candidates = retrieve_candidates(q)
        results = final_rank(q, candidates)
        extra_queries = multi_hop_queries(q, results[:5])
        for eq in extra_queries:
            extra_candidates = retrieve_candidates(eq, per_query_k=40)
            candidates.extend(extra_candidates)
        results = final_rank(q, list(set(candidates)))
        for text, page, score in results[:5]:
            print(f"\nPage {page} | final_score={score:.3f}")
            print(text[:700])
            print("-" * 70)