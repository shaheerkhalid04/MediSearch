"""
main.py – MediSearch demo runner

Run:  python main.py
"""

from graph import SymptomConditionGraph
from search import MediSearch


def print_results(engine: MediSearch, symptoms: list[str], top_k: int = 5):
    print("\n" + "=" * 60)
    print(f"Query symptoms: {symptoms}")
    print("=" * 60)
    results = engine.query(symptoms, top_k=top_k)
    if not results:
        print("No matching conditions found.")
        return
    for rank, r in enumerate(results, 1):
        print(f"\nRank #{rank}")
        print(engine.explain(r))
    print("\n[Disclaimer] Results are informational only. Consult a health professional.")


def main():
    graph  = SymptomConditionGraph()
    engine = MediSearch(graph)

    graph.stats()

    # --- Test cases ---

    # Classic flu presentation
    print_results(engine, ["fever", "body_aches", "chills", "fatigue", "headache"])

    # Cold vs allergies overlap
    print_results(engine, ["runny_nose", "sneezing", "cough", "fatigue"])

    # COVID-19 distinctive symptoms
    print_results(engine, ["loss_of_smell", "loss_of_taste", "fever", "fatigue"])

    # Migraine
    print_results(engine, ["severe_headache", "nausea", "light_sensitivity", "vomiting"])

    # Anxiety
    print_results(engine, ["rapid_heartbeat", "chest_tightness", "difficulty_focusing", "sleep_disturbance"])

    # Ambiguous overlap test (dehydration vs stress headache vs migraine)
    print_results(engine, ["headache", "fatigue", "nausea", "dizziness"])

    # Autocomplete demo
    print("\n--- Symptom autocomplete: 'fa' ---")
    print(engine.suggest_symptoms("fa"))


if __name__ == "__main__":
    main()
