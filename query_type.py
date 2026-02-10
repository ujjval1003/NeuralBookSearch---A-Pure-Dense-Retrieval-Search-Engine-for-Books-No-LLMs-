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

def is_comparison(query: str) -> bool:
    q = query.lower()
    patterns = [
        r"\bdifference\b",
        r"\bcompare\b",
        r"\bvs\b",
        r"\bversus\b",
        r"\badvantages\b",
        r"\bdisadvantages\b",
        r"\bpros\b",
        r"\bcons\b",
        r"\bbetter than\b",
    ]
    return any(re.search(p, q) for p in patterns)