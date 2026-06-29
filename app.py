from flask import Flask, render_template, request, jsonify
from graph import SymptomConditionGraph
from search import MediSearch

app = Flask(__name__)

# Initialize the AI Engine
graph = SymptomConditionGraph()
engine = MediSearch(graph)
graph.stats()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/suggest")
def suggest():
    q = request.args.get("q", "").lower()
    if not q:
        return jsonify([])
    suggestions = engine.suggest_symptoms(q)
    return jsonify(suggestions)

@app.route("/api/query", methods=["POST"])
def query():
    data = request.json
    symptoms = data.get("symptoms", [])
    if not symptoms:
        return jsonify([])
    
    results = engine.query(symptoms, top_k=5)
    
    # Format the results to return as JSON
    response = []
    for r in results:
        response.append({
            "condition": r.condition,
            "final_score": r.final_score,
            "coverage_ratio": r.coverage_ratio,
            "matched_symptoms": r.matched_symptoms,
            "total_condition_symptoms": r.total_condition_symptoms,
            # Let's also include the description from the graph
            "description": graph.G.nodes[r.condition].get("description", "")
        })
        
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
