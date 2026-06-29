"""
graph.py – Symptom-Condition Knowledge Graph
Nodes: symptoms (type='symptom') | conditions (type='condition')
Edges: weighted associations derived from dataset (synthetic for now)
"""

import networkx as nx
import json


class SymptomConditionGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.load_from_json("graph_data.json")

    # ------------------------------------------------------------------ #
    #  Graph Construction                                                  #
    # ------------------------------------------------------------------ #

    def add_symptom(self, name: str):
        self.G.add_node(name, type="symptom")

    def add_condition(self, name: str, description: str = ""):
        self.G.add_node(name, type="condition", description=description)

    def add_association(self, symptom: str, condition: str, weight: float):
        """
        weight: 0.0–1.0 – strength of symptom→condition association.
        Derived from co-occurrence frequency in the dataset.
        """
        if symptom not in self.G:
            self.add_symptom(symptom)
        if condition not in self.G:
            self.add_condition(condition)
        self.G.add_edge(symptom, condition, weight=round(weight, 3))

    def load_from_json(self, path: str):
        """Load graph from a JSON file once real survey data is processed."""
        with open(path) as f:
            data = json.load(f)
        for s in data.get("symptoms", []):
            self.add_symptom(s)
        for c in data.get("conditions", []):
            self.add_condition(c["name"], c.get("description", ""))
        for edge in data.get("associations", []):
            self.add_association(edge["symptom"], edge["condition"], edge["weight"])

    # ------------------------------------------------------------------ #
    #  Synthetic Data (replace with real survey-derived data later)       #
    # ------------------------------------------------------------------ #

    def _build_synthetic_graph(self):
        """
        Synthetic associations for common student-population conditions.
        Weights are manually estimated; will be replaced by co-occurrence
        frequencies computed from the actual survey dataset.
        """
        associations = [
            # (symptom, condition, weight)

            # --- Influenza ---
            ("fever",              "Influenza",          0.90),
            ("body_aches",         "Influenza",          0.85),
            ("fatigue",            "Influenza",          0.80),
            ("headache",           "Influenza",          0.70),
            ("chills",             "Influenza",          0.75),
            ("cough",              "Influenza",          0.65),
            ("sore_throat",        "Influenza",          0.55),
            ("runny_nose",         "Influenza",          0.50),

            # --- Common Cold ---
            ("runny_nose",         "Common Cold",        0.90),
            ("sore_throat",        "Common Cold",        0.80),
            ("sneezing",           "Common Cold",        0.85),
            ("cough",              "Common Cold",        0.70),
            ("mild_fever",         "Common Cold",        0.50),
            ("fatigue",            "Common Cold",        0.45),
            ("headache",           "Common Cold",        0.40),

            # --- Stress Headache ---
            ("headache",           "Stress Headache",    0.90),
            ("neck_tension",       "Stress Headache",    0.80),
            ("fatigue",            "Stress Headache",    0.70),
            ("difficulty_focusing","Stress Headache",    0.65),
            ("irritability",       "Stress Headache",    0.60),
            ("eye_strain",         "Stress Headache",    0.55),

            # --- Migraine ---
            ("severe_headache",    "Migraine",           0.95),
            ("nausea",             "Migraine",           0.80),
            ("light_sensitivity",  "Migraine",           0.85),
            ("sound_sensitivity",  "Migraine",           0.80),
            ("vomiting",           "Migraine",           0.65),
            ("visual_disturbance", "Migraine",           0.70),
            ("fatigue",            "Migraine",           0.50),

            # --- Gastroenteritis ---
            ("nausea",             "Gastroenteritis",    0.85),
            ("vomiting",           "Gastroenteritis",    0.85),
            ("diarrhea",           "Gastroenteritis",    0.90),
            ("stomach_cramps",     "Gastroenteritis",    0.80),
            ("fever",              "Gastroenteritis",    0.55),
            ("loss_of_appetite",   "Gastroenteritis",    0.70),
            ("fatigue",            "Gastroenteritis",    0.50),

            # --- Mononucleosis (Mono) ---
            ("extreme_fatigue",    "Mononucleosis",      0.95),
            ("sore_throat",        "Mononucleosis",      0.85),
            ("swollen_lymph_nodes","Mononucleosis",      0.90),
            ("fever",              "Mononucleosis",      0.75),
            ("body_aches",         "Mononucleosis",      0.65),
            ("loss_of_appetite",   "Mononucleosis",      0.55),
            ("rash",               "Mononucleosis",      0.40),

            # --- Seasonal Allergies ---
            ("sneezing",           "Seasonal Allergies", 0.90),
            ("runny_nose",         "Seasonal Allergies", 0.85),
            ("itchy_eyes",         "Seasonal Allergies", 0.90),
            ("watery_eyes",        "Seasonal Allergies", 0.85),
            ("nasal_congestion",   "Seasonal Allergies", 0.80),
            ("cough",              "Seasonal Allergies", 0.45),
            ("fatigue",            "Seasonal Allergies", 0.40),

            # --- Anxiety ---
            ("difficulty_focusing","Anxiety",            0.75),
            ("irritability",       "Anxiety",            0.70),
            ("fatigue",            "Anxiety",            0.65),
            ("rapid_heartbeat",    "Anxiety",            0.80),
            ("chest_tightness",    "Anxiety",            0.75),
            ("shortness_of_breath","Anxiety",            0.65),
            ("sleep_disturbance",  "Anxiety",            0.80),
            ("headache",           "Anxiety",            0.50),

            # --- Dehydration ---
            ("headache",           "Dehydration",        0.75),
            ("fatigue",            "Dehydration",        0.70),
            ("dizziness",          "Dehydration",        0.85),
            ("dry_mouth",          "Dehydration",        0.90),
            ("dark_urine",         "Dehydration",        0.85),
            ("muscle_cramps",      "Dehydration",        0.65),
            ("nausea",             "Dehydration",        0.50),

            # --- COVID-19 ---
            ("fever",              "COVID-19",           0.80),
            ("cough",              "COVID-19",           0.80),
            ("fatigue",            "COVID-19",           0.75),
            ("loss_of_smell",      "COVID-19",           0.90),
            ("loss_of_taste",      "COVID-19",           0.88),
            ("shortness_of_breath","COVID-19",           0.70),
            ("body_aches",         "COVID-19",           0.65),
            ("sore_throat",        "COVID-19",           0.55),
            ("headache",           "COVID-19",           0.55),
            ("chills",             "COVID-19",           0.60),
        ]

        for symptom, condition, weight in associations:
            self.add_association(symptom, condition, weight)

    # ------------------------------------------------------------------ #
    #  Accessors                                                           #
    # ------------------------------------------------------------------ #

    def get_symptoms(self) -> list:
        return [n for n, d in self.G.nodes(data=True) if d["type"] == "symptom"]

    def get_conditions(self) -> list:
        return [n for n, d in self.G.nodes(data=True) if d["type"] == "condition"]

    def neighbors_of(self, node: str) -> dict:
        """Return {neighbor: weight} for all edges of a node."""
        return {nbr: self.G[node][nbr]["weight"] for nbr in self.G.neighbors(node)}

    def stats(self):
        symptoms  = len(self.get_symptoms())
        conditions = len(self.get_conditions())
        edges     = self.G.number_of_edges()
        print(f"Graph stats → symptoms: {symptoms} | conditions: {conditions} | edges: {edges}")
