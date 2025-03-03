import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_process_clubs(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    
    descriptions = []
    valid_items = []
    for item in data:
        if "description" in item and item["description"]:
            descriptions.append(item["description"].lower())
            valid_items.append(item)
    return descriptions, valid_items

def get_recommendations(descriptions, valid_items, user_query, top_k=3):
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
    for idx in top_indices[0:top_k]:
        if similarities[idx] > 0:
            results.append((valid_items[idx], similarities[idx]))
    return results

def get_sports_recommendations(descriptions, valid_items, user_query, top_k=3):
    # Sport-specific keyword mappings
    sport_keywords = {
        'running': ['run', 'running', 'track', 'marathon'],
        'combat': ['combat', 'fighting', 'martial arts', 'boxing', 'jiu-jitsu', 'bjj', 'mma', 'karate', 'wrestling'],
        'boxing': ['box', 'boxing', 'combat'],
        'jiu-jitsu': ['bjj', 'jiu-jitsu', 'grappling', 'brazilian'],
    }
    
    # Break down the query into components
    query_lower = user_query.lower()
    matched_clubs = {}
    total_score = {}
    
    # Create enhanced descriptions
    enhanced_descriptions = []
    for item in valid_items:
        name = item['name'].lower()
        desc = item['description'].lower()
        enhanced_desc = f"{name} {name} {desc}"
        enhanced_descriptions.append(enhanced_desc)
    
    # Process each potential sport category
    for sport, keywords in sport_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            # Configure vectorizer for this sport category
            vectorizer = TfidfVectorizer(
                stop_words='english',
                max_df=0.8,
                min_df=1,
                ngram_range=(1, 2)
            )
            
            # Add sport-specific emphasis to the query
            enhanced_query = f"{sport} {' '.join(keywords)} {user_query}".lower()
            
            # Fit and transform
            vectors = vectorizer.fit_transform(enhanced_descriptions)
            user_vector = vectorizer.transform([enhanced_query])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, vectors).flatten()
            
            # Add exact name match bonus
            for idx, item in enumerate(valid_items):
                club_name = item['name'].lower()
                # Add bonus for exact sport name match
                if sport in club_name or any(keyword in club_name for keyword in keywords):
                    similarities[idx] += 0.5
                
                # Store the highest score for each club
                if idx not in total_score or similarities[idx] > total_score[idx]:
                    total_score[idx] = similarities[idx]
                    matched_clubs[idx] = item
    
    # Sort clubs by their highest scores
    sorted_clubs = sorted([(idx, score) for idx, score in total_score.items()], 
                         key=lambda x: x[1], reverse=True)
    
    # Get top-k unique clubs
    results = []
    seen_names = set()
    for idx, score in sorted_clubs:
        club = matched_clubs[idx]
        if club['name'] not in seen_names and score > 0:
            results.append((club, score))
            seen_names.add(club['name'])
            if len(results) >= top_k:
                break
    
    return results

# Load regular clubs
regular_descriptions, regular_clubs = load_and_process_clubs("HOTH XII Orgs.json")

# Load sports clubs
sports_descriptions, sports_clubs = load_and_process_clubs("UCLA Club Sports.json")

# Get user input for regular clubs
print("\n=== Regular Clubs Search ===")
regular_query = input("What kind of clubs are you interested in? ")
regular_results = get_recommendations(regular_descriptions, regular_clubs, regular_query, top_k=3)

# Get user input for sports
print("\n=== Sports Clubs Search ===")
sports_query = input("What sports or athletic activities interest you? ")
sports_results = get_sports_recommendations(sports_descriptions, sports_clubs, sports_query, top_k=3)

# Display regular club results
if regular_results:
    print("\n=== Top 3 Recommended Regular Clubs ===")
    for club, score in regular_results:
        print(f"\nClub: {club['name']} (Score: {score:.4f})")
        print(f"Description: {club['description']}")
        print("-" * 50)
else:
    print("\nNo matching regular clubs found.")

# Display sports club results
if sports_results:
    print("\n=== Top 3 Recommended Sports Clubs ===")
    for club, score in sports_results:
        print(f"\nClub: {club['name']} (Score: {score:.4f})")
        print(f"Description: {club['description']}")
        print("-" * 50)
else:
    print("\nNo matching sports clubs found.") 