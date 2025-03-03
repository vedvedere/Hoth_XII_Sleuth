from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load and process clubs
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

# Get recommendations for regular clubs
def get_recommendations(descriptions, valid_items, user_query, top_k=5):  # Change top_k to 5
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

# Get recommendations for sports clubs
def get_sports_recommendations(descriptions, valid_items, user_query, top_k=5):  # Change top_k to 5
    sport_keywords = {
        'running': ['run', 'running', 'track', 'marathon'],
        'combat': ['combat', 'fighting', 'martial arts', 'boxing', 'jiu-jitsu', 'bjj', 'mma', 'karate', 'wrestling'],
        'boxing': ['box', 'boxing', 'combat'],
        'jiu-jitsu': ['bjj', 'jiu-jitsu', 'grappling', 'brazilian'],
    }
    
    query_lower = user_query.lower()
    matched_clubs = {}
    total_score = {}
    
    enhanced_descriptions = []
    for item in valid_items:
        name = item['name'].lower()
        desc = item['description'].lower()
        enhanced_desc = f"{name} {name} {desc}"
        enhanced_descriptions.append(enhanced_desc)
    
    for sport, keywords in sport_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_df=0.8,
                min_df=1,
                ngram_range=(1, 2)
            )
            
            enhanced_query = f"{sport} {' '.join(keywords)} {user_query}".lower()
            
            vectors = vectorizer.fit_transform(enhanced_descriptions)
            user_vector = vectorizer.transform([enhanced_query])
            
            similarities = cosine_similarity(user_vector, vectors).flatten()
            
            for idx, item in enumerate(valid_items):
                club_name = item['name'].lower()
                if sport in club_name or any(keyword in club_name for keyword in keywords):
                    similarities[idx] += 0.5
                
                if idx not in total_score or similarities[idx] > total_score[idx]:
                    total_score[idx] = similarities[idx]
                    matched_clubs[idx] = item
    
    sorted_clubs = sorted([(idx, score) for idx, score in total_score.items()], 
                         key=lambda x: x[1], reverse=True)
    
    results = []
    seen_names = set()
    for idx, score in sorted_clubs:
        club = matched_clubs[idx]
        if club['name'] not in seen_names and score > 0:
            results.append((club, float(score)))  # Convert numpy float to Python float
            seen_names.add(club['name'])
            if len(results) >= top_k:  # Return top 5 recommendations
                break
    
    return results

# Load regular and sports clubs
regular_descriptions, regular_clubs = load_and_process_clubs("HOTH XII Orgs.json")
sports_descriptions, sports_clubs = load_and_process_clubs("UCLA Club Sports.json")

# Endpoint to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    # Get the payload sent from the frontend
    payload = request.data.decode('utf-8')  # Decode the bytes to a string
    print('Received payload:', payload)

    # Get recommendations for regular clubs
    regular_results = get_recommendations(regular_descriptions, regular_clubs, payload, top_k=5)  # Change top_k to 5
    # Get recommendations for sports clubs
    sports_results = get_sports_recommendations(sports_descriptions, sports_clubs, payload, top_k=5)  # Change top_k to 5

    # Format the results for the frontend
    response = {
        'status': 'success',
        'message': 'Recommendations generated successfully!',
        'regular_clubs': [{
            'name': club['name'],
            'description': club['description'],
            'score': score
        } for club, score in regular_results],
        'sports_clubs': [{
            'name': club['name'],
            'description': club['description'],
            'score': score
        } for club, score in sports_results],
    }
    return jsonify(response)

# Start the server
if __name__ == '__main__':
    app.run(port=3000)