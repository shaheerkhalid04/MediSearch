# MediSearch: A Symptom-Based Condition Search System

Hey! Welcome to the MediSearch project repository for COMP360. This is our final submission.

Our project is an AI-powered heuristic search engine designed to help university students map their symptoms to possible conditions. We built a custom knowledge graph using Python's NetworkX based on simulated student survey data.

## What's in here?

- `app.py`: The main Flask web server that powers the frontend.
- `graph.py` & `search.py`: The core AI logic (Best-First Search over our Knowledge Graph).
- `generate_dataset.py`: The script we used to simulate the 1,000 student survey responses and calculate the conditional probabilities.
- `survey_responses.csv`: The raw simulated dataset acting as our survey results.
- `graph_data.json`: The processed knowledge graph nodes and edge weights.
- `templates/` & `static/`: The HTML, CSS, and JS files for our modern web interface.

## How to Run the Project

Running the project is super straightforward! Just follow these steps:

1. **Install Dependencies**: Make sure you have Python installed, then install Flask (and networkx if you haven't already):
   ```bash
   pip install flask networkx
   ```

2. **Start the Server**: In your terminal, navigate to this folder and run:
   ```bash
   python app.py
   ```

3. **Open the App**: Once the server starts, open your favorite web browser and go to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

That's it! You can start typing symptoms into the search bar, select the ones you're experiencing, and hit "Analyze Symptoms" to see the AI in action.

Enjoy exploring MediSearch!
