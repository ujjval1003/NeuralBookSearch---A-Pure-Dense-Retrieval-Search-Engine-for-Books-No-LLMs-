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
from query_expand import expand_query

def extract_concepts(texts):
    concepts = set()
    for text, _, _ in texts:
        matches = re.findall(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*\ssearch)', text)
        for m in matches:
            if len(m) > 4:
                concepts.add(m.lower())
        eq = re.findall(r'f\(n\)\s*=\s*[gh]\(n\)', text)
        concepts.update(eq)
    return list(concepts)

def multi_hop_queries(first_results):
    concepts = extract_concepts(first_results)
    new_queries = []
    for c in concepts:
        new_queries.extend(expand_query(c))
    return list(set(new_queries))