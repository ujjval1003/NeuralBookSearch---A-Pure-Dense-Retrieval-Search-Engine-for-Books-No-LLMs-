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
import numpy as np
import pickle

DB_CONFIG = {
    "host": "db.YOUR_DB_NAME.supabase.co",
    "database": "postgres",
    "user": "postgres",
    "password": "YOUR_PASSWORD",
    "port": 5432,
}

def build_index():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT content, page_number, embedding FROM book_chunks;")
    texts = []
    pages = []
    vectors = []
    lookup = {}
    for i, (content, page, emb) in enumerate(cur.fetchall()):
        texts.append(content)
        pages.append(page)
        emb = emb.strip("[]")
        emb = [float(x) for x in emb.split(",")]
        vectors.append(emb)
        lookup[(content, page)] = i
    conn.close()
    vectors = np.array(vectors, dtype=np.float32)
    data = {
        "texts": texts,
        "pages": pages,
        "vectors": vectors,
        "lookup": lookup
    }
    with open("../local_index.pkl", "wb") as f:
        pickle.dump(data, f)
    print("Local neural index built. Total passages:", len(texts))

if __name__ == "__main__":
    build_index()