"""
search.py – MediSearch Heuristic Search Engine

Algorithm: Best-First Search over the symptom-condition knowledge graph.

Heuristic h(c, S):
    h(c, S) = Σ w(s, c)  for all s ∈ S where edge(s, c) exists

    Raw score is further normalized by:
    - Symptom coverage ratio:  matched_symptoms / total_input_symptoms
    - Condition coverage ratio: matched_symptoms / total_symptoms_for_condition

Final score combines both to avoid bias toward conditions with very many
symptoms (which would accumulate score even on partial matches).
"""

import heapq
from dataclasses import dataclass, field
from graph import SymptomConditionGraph


@dataclass
class SearchResult:
    condition:        str
    raw_score:        float   # Σ edge weights for matched symptoms
    final_score:      float   # normalized composite score
    matched_symptoms: list    # which input symptoms matched
    total_condition_symptoms: int  # total symptoms linked to this condition in graph
    coverage_ratio:   float   # matched / total_input_symptoms

    def __lt__(self, other):
        return self.final_score > other.final_score  # max-heap ordering


class MediSearch:
    def __init__(self, graph: SymptomConditionGraph):
        self.graph = graph

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def query(self, symptoms: list[str], top_k: int = 5) -> list[SearchResult]:
        """
        Given a list of symptom strings, return top_k ranked conditions.

        Steps:
        1. Validate + normalize input symptoms against graph nodes.
        2. For each input symptom, traverse edges to condition nodes.
        3. Accumulate h(c, S) per condition.
        4. Normalize and rank using a max-heap.
        5. Return top_k SearchResult objects.
        """
        # Step 1 – validate symptoms
        valid_symptoms, unknown = self._validate(symptoms)
        if unknown:
            print(f"[warn] unknown symptoms (not in graph): {unknown}")
        if not valid_symptoms:
            return []

        # Step 2 & 3 – traverse edges, accumulate scores
        scores: dict[str, float] = {}
        matched: dict[str, list] = {}

        for symptom in valid_symptoms:
            neighbors = self.graph.neighbors_of(symptom)
            for node, weight in neighbors.items():
                if self.graph.G.nodes[node]["type"] == "condition":
                    scores[node]  = scores.get(node, 0.0) + weight
                    matched[node] = matched.get(node, []) + [symptom]

        if not scores:
            return []

        # Step 4 – normalize + push into max-heap
        n_input = len(valid_symptoms)
        heap: list[SearchResult] = []

        for condition, raw_score in scores.items():
            matched_syms = matched[condition]
            n_matched     = len(matched_syms)

            # How many of the INPUT symptoms matched this condition
            coverage_ratio = n_matched / n_input

            # How many of the condition's own symptoms were covered
            total_cond_syms = sum(
                1 for nbr in self.graph.G.neighbors(condition)
                if self.graph.G.nodes[nbr]["type"] == "symptom"
            )
            specificity_ratio = n_matched / total_cond_syms if total_cond_syms else 0.0

            # Final score: weighted combination
            # 0.6 × raw_score favours strong individual edges
            # 0.4 × coverage_ratio × raw_score penalises low-coverage matches
            final_score = round(
                0.6 * raw_score + 0.4 * coverage_ratio * raw_score, 4
            )

            result = SearchResult(
                condition=condition,
                raw_score=round(raw_score, 4),
                final_score=final_score,
                matched_symptoms=matched_syms,
                total_condition_symptoms=total_cond_syms,
                coverage_ratio=round(coverage_ratio, 3),
            )
            heapq.heappush(heap, result)

        # Step 5 – extract top_k
        top = heapq.nsmallest(top_k, heap)  # __lt__ is reversed → nsmallest = highest score
        return top

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _validate(self, symptoms: list[str]) -> tuple[list, list]:
        graph_symptoms = set(self.graph.get_symptoms())
        valid   = [s for s in symptoms if s in graph_symptoms]
        unknown = [s for s in symptoms if s not in graph_symptoms]
        return valid, unknown

    def suggest_symptoms(self, partial: str) -> list[str]:
        """Simple prefix match for UI autocomplete."""
        return [s for s in self.graph.get_symptoms() if s.startswith(partial)]

    def explain(self, result: SearchResult) -> str:
        lines = [
            f"Condition      : {result.condition}",
            f"Final Score    : {result.final_score}",
            f"Raw Score      : {result.raw_score}",
            f"Coverage       : {result.coverage_ratio:.0%} of input symptoms matched",
            f"Matched        : {', '.join(result.matched_symptoms)}",
            f"Cond. symptoms : {result.total_condition_symptoms} total in graph",
        ]
        return "\n".join(lines)
