import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load the JSON data
# If you have clubs.json in the same directory, do:
with open("HOTH XII Orgs.json", "r") as f:
    clubs_data = json.load(f)

# 2. Extract the descriptions
# Add error handling for missing descriptions
club_descriptions = []
valid_clubs = []
for club in clubs_data:
    if "description" in club and club["description"]:  # Check if description exists and is not empty
        club_descriptions.append(club["description"].lower())  # Convert to lowercase
        valid_clubs.append(club)

# 3. Fit TF-IDF model with different parameters
vectorizer = TfidfVectorizer(
    stop_words='english',  # Remove common English words
    max_df=0.7,           # Ignore terms that appear in more than 70% of documents
    ngram_range=(1, 2)    # Consider both single words and pairs of words
)
club_vectors = vectorizer.fit_transform(club_descriptions)

# 4. Get user input interactively
user_query = input("Enter your search query: ")
user_vector = vectorizer.transform([user_query.lower()])

# 5. Compute similarity scores
similarities = cosine_similarity(user_vector, club_vectors).flatten()

# 6. Sort and display results
top_indices = np.argsort(similarities)[::-1]
for idx in top_indices[0:10]:
    club_name = valid_clubs[idx]["name"]
    description = valid_clubs[idx]["description"]
    score = similarities[idx]
    if score > 0:  # Only show results with positive similarity
        print(f"\nClub: {club_name} (Score: {score:.4f})")
        print(f"Description: {description}")
        print("-" * 50)