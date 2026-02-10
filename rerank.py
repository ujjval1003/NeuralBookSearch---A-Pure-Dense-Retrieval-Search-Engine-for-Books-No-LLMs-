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

import numpy as np
import pickle
from fastembed import TextEmbedding

embedder = TextEmbedding("BAAI/bge-small-en-v1.5", providers=["CUDAExecutionProvider"]) # Remove providers=["CUDAExecutionProvider"] if you don't have NVIDIA GPU

with open("../local_index.pkl", "rb") as f:
    index_data = pickle.load(f)

texts = index_data["texts"]
pages = index_data["pages"]
vectors = index_data["vectors"]
lookup = index_data["lookup"]
vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

def rerank(query, candidates):
    q_emb = list(embedder.embed([f"query: {query}"]))[0].astype(np.float32)
    q_emb = q_emb / np.linalg.norm(q_emb)
    idxs = [lookup[(text, page)] for text, page in candidates if (text, page) in lookup]
    candidate_vectors = vectors[idxs]
    scores = np.dot(candidate_vectors, q_emb)
    ranked = sorted(
        [(texts[idxs[i]], pages[idxs[i]], float(scores[i]))
         for i in range(len(idxs))],
        key=lambda x: x[2],
        reverse=True
    )
    return ranked[:20]