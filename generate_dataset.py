import json
import random

SYMPTOMS = [
    "fever", "chills", "cough", "runny_nose", "sneezing", "fatigue", 
    "headache", "severe_headache", "body_aches", "loss_of_smell", 
    "loss_of_taste", "nausea", "vomiting", "dizziness", "light_sensitivity", 
    "rapid_heartbeat", "chest_tightness", "difficulty_focusing", "sleep_disturbance"
]

CONDITIONS = {
    "Influenza": {"desc": "A viral infection that attacks your respiratory system."},
    "COVID-19": {"desc": "An infectious disease caused by the SARS-CoV-2 virus."},
    "Common Cold": {"desc": "A viral infection of your nose and throat."},
    "Seasonal Allergies": {"desc": "An allergic response causing itchy, watery eyes, sneezing and other similar symptoms."},
    "Migraine": {"desc": "A headache that can cause severe throbbing pain or a pulsing sensation."},
    "Anxiety": {"desc": "A mental health disorder characterized by feelings of worry, anxiety, or fear."},
    "Dehydration": {"desc": "A condition caused by the loss of too much fluid from the body."},
    "Gastroenteritis": {"desc": "An intestinal infection marked by diarrhea, cramps, nausea, vomiting and fever."},
    "Mononucleosis": {"desc": "An infectious illness that's usually caused by the Epstein-Barr virus."},
    "Stress Headache": {"desc": "A mild to moderate pain that's often described as feeling like a tight band around the head."}
}

# Probabilities of a symptom given a condition (for synthetic data generation)
PROFILES = {
    "Influenza": {"fever": 0.9, "chills": 0.8, "fatigue": 0.9, "body_aches": 0.85, "cough": 0.7, "headache": 0.7, "runny_nose": 0.4},
    "COVID-19": {"fever": 0.85, "cough": 0.8, "fatigue": 0.8, "loss_of_smell": 0.9, "loss_of_taste": 0.88, "body_aches": 0.6, "headache": 0.6},
    "Common Cold": {"runny_nose": 0.9, "sneezing": 0.85, "cough": 0.75, "fatigue": 0.4, "headache": 0.3},
    "Seasonal Allergies": {"sneezing": 0.9, "runny_nose": 0.85, "cough": 0.3, "fatigue": 0.3},
    "Migraine": {"severe_headache": 0.95, "nausea": 0.7, "vomiting": 0.4, "light_sensitivity": 0.9, "dizziness": 0.5},
    "Anxiety": {"rapid_heartbeat": 0.85, "chest_tightness": 0.7, "difficulty_focusing": 0.75, "sleep_disturbance": 0.8, "fatigue": 0.6},
    "Dehydration": {"headache": 0.7, "dizziness": 0.8, "fatigue": 0.75, "rapid_heartbeat": 0.4},
    "Gastroenteritis": {"nausea": 0.9, "vomiting": 0.85, "fever": 0.5, "fatigue": 0.6, "chills": 0.4},
    "Mononucleosis": {"fatigue": 0.95, "fever": 0.7, "body_aches": 0.6, "headache": 0.5},
    "Stress Headache": {"headache": 0.85, "fatigue": 0.7, "difficulty_focusing": 0.6, "sleep_disturbance": 0.5}
}

def generate_responses(num_samples=1000):
    responses = []
    for _ in range(num_samples):
        # Pick a random condition based on uniform distribution for simplicity
        condition = random.choice(list(CONDITIONS.keys()))
        
        # User experiences symptoms based on the true profiles with some noise
        profile = PROFILES.get(condition, {})
        experienced_symptoms = []
        for sym in SYMPTOMS:
            prob = profile.get(sym, 0.05) # 5% chance of random unrelated symptom
            if random.random() < prob:
                experienced_symptoms.append(sym)
                
        # Ensure at least one symptom
        if not experienced_symptoms:
            experienced_symptoms.append(random.choice(list(profile.keys()) if profile else SYMPTOMS))
            
        responses.append({
            "diagnosis": condition,
            "symptoms": experienced_symptoms
        })
    return responses

def process_data(responses):
    # Count occurrences
    cond_counts = {c: 0 for c in CONDITIONS}
    sym_cond_counts = {c: {s: 0 for s in SYMPTOMS} for c in CONDITIONS}
    
    for r in responses:
        c = r["diagnosis"]
        cond_counts[c] += 1
        for s in r["symptoms"]:
            sym_cond_counts[c][s] += 1
            
    # Calculate weights P(Symptom | Condition)
    associations = []
    for c in CONDITIONS:
        total_c = cond_counts[c]
        if total_c == 0: continue
        for s in SYMPTOMS:
            count_s_c = sym_cond_counts[c][s]
            weight = count_s_c / total_c
            if weight > 0.1: # Only keep meaningful associations
                associations.append({
                    "symptom": s,
                    "condition": c,
                    "weight": round(weight, 3)
                })
                
    return associations

def main():
    print("Generating simulated survey responses...")
    responses = generate_responses(1000)
    print(f"Generated {len(responses)} responses.")
    
    import csv
    with open("survey_responses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Response_ID", "Diagnosis", "Symptoms"])
        for i, r in enumerate(responses, 1):
            writer.writerow([i, r["diagnosis"], ", ".join(r["symptoms"])])
    print("Exported raw responses to survey_responses.csv")
    
    print("Processing data into knowledge graph weights...")
    associations = process_data(responses)
    
    graph_data = {
        "symptoms": SYMPTOMS,
        "conditions": [{"name": k, "description": v["desc"]} for k, v in CONDITIONS.items()],
        "associations": associations
    }
    
    with open("graph_data.json", "w") as f:
        json.dump(graph_data, f, indent=4)
        
    print(f"Exported graph data with {len(SYMPTOMS)} symptoms, {len(CONDITIONS)} conditions, and {len(associations)} edges to graph_data.json.")

if __name__ == "__main__":
    main()
