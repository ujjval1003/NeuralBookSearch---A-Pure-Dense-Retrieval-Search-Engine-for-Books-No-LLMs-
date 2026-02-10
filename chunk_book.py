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

import re

def clean_text(text):
    """
    Removes textbook headers, footers, and formatting noise.
    This massively improves embedding quality.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\b\d{1,4}\b", " ", text)
    text = re.sub(r"(Section|Chapter)\s+\d+(\.\d+)?", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"Artificial Intelligence: A Modern Approach", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"(Figure|Fig\.|Table)\s+\d+(\.\d+)?", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(pages, chunk_size=220, overlap=60):
    """
    Creates overlapping semantic chunks from textbook pages.
    """
    chunks = []
    for page_number, text in pages:
        text = clean_text(text)
        words = text.split()
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk = " ".join(chunk_words)
            if len(chunk) > 120:
                chunks.append((page_number, chunk))
            start += chunk_size - overlap
    return chunks