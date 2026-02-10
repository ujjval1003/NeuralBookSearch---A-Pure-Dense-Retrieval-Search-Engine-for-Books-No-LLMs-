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

def build_comparison_answer(comparison_data):
    answer = "\n\nFINAL EXPLANATION\n"
    answer += "-"*40 + "\n"
    concepts = list(comparison_data.keys())
    if len(concepts) < 2:
        return None
    c1, c2 = concepts[0], concepts[1]
    answer += f"\n{c1.upper()}:\n"
    for text, page, _ in comparison_data[c1][:2]:
        answer += f"- {text.strip()}\n"
    answer += f"\n{c2.upper()}:\n"
    for text, page, _ in comparison_data[c2][:2]:
        answer += f"- {text.strip()}\n"
    answer += "\nKey Difference:\n"
    answer += f"{c1} focuses on path cost (g(n)) while {c2} focuses on heuristic estimate (h(n)).\n"
    return answer