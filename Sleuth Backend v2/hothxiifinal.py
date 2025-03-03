from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load and process the club masterlist
def load_and_process_clubs(file_path):
    with open(file_path, "r", encoding="utf-8") as f:  # Use UTF-8 encoding
        data = json.load(f)
    
    descriptions = []
    valid_items = []
    for item in data:
        if "description" in item and item["description"]:
            descriptions.append(item["description"].lower())
            valid_items.append(item)
    return descriptions, valid_items

# Get recommendations for clubs
def get_recommendations(descriptions, valid_items, user_query, top_k=5):
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_df=0.7,
        ngram_range=(1, 2)
    )
    vectors = vectorizer.fit_transform(descriptions)
    user_vector = vectorizer.transform([user_query.lower()])
    
    similarities = cosine_similarity(user_vector, vectors).flatten()
    top_indices = np.argsort(similarities)[::-1]
    
    results = []
    for idx in top_indices[0:top_k]:  # Return top 5 recommendations
        if similarities[idx] > 0:
            results.append((valid_items[idx], float(similarities[idx])))  # Convert numpy float to Python float
    return results

# Load the club masterlist
club_descriptions, club_items = load_and_process_clubs("UCLA Club Masterlist.json")

# Endpoint to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    # Get the payload sent from the frontend
    payload = request.data.decode('utf-8')  # Decode the bytes to a string
    print('Received payload:', payload)

    # Get recommendations for clubs
    recommendations = get_recommendations(club_descriptions, club_items, payload, top_k=5)

    # Format the results for the frontend
    response = {
        'status': 'success',
        'message': 'Recommendations generated successfully!',
        'clubs': [{
            'name': club['name'],
            'description': club['description'],
            'score': score
        } for club, score in recommendations],
    }
    return jsonify(response)

# Start the server
if __name__ == '__main__':
    app.run(port=3000)