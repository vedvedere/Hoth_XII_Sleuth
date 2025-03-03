from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Add a test route
@app.route('/', methods=['GET'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sleuth - Find Your Future</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * { 
                margin: 0; 
                padding: 0; 
                box-sizing: border-box; 
                font-family: 'Inter', sans-serif;
                scroll-behavior: smooth;
            }
            
            body { 
                min-height: 100vh;
                background: linear-gradient(135deg, #2774AE 0%, #FFD100 100%);
            }
            
            section {
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 40px 20px;
                position: relative;
            }
            
            .hero {
                text-align: center;
                position: relative;
            }
            
            .scroll-indicator {
                position: absolute;
                bottom: 40px;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                font-size: 2em;
                animation: bounce 2s infinite;
                cursor: pointer;
                text-decoration: none;
            }
            
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% {
                    transform: translateY(0) translateX(-50%);
                }
                40% {
                    transform: translateY(-30px) translateX(-50%);
                }
                60% {
                    transform: translateY(-15px) translateX(-50%);
                }
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 600px;
                text-align: center;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            .features {
                background: rgba(39, 116, 174, 0.1);
                backdrop-filter: blur(10px);
            }
            
            .features-container {
                max-width: 1200px;
                width: 100%;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 30px;
                padding: 0 20px;
            }
            
            .feature-card {
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 20px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
            }
            
            .feature-icon {
                font-size: 3em;
                color: #2774AE;
                margin-bottom: 20px;
            }
            
            .feature-title {
                color: #2774AE;
                font-size: 1.5em;
                margin-bottom: 15px;
                font-weight: 600;
            }
            
            .feature-description {
                color: #4a5568;
                line-height: 1.6;
            }
            
            h1 { 
                color: #2774AE;
                font-size: 3.5em;
                margin-bottom: 10px;
                font-weight: 700;
            }
            
            .motto {
                color: #2774AE;
                font-size: 1.8em;
                margin-bottom: 30px;
                font-weight: 500;
            }
            
            .form-container { 
                margin-bottom: 20px;
            }
            
            input[type="text"] { 
                width: 100%;
                padding: 15px 20px;
                margin-bottom: 20px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                font-size: 1em;
                transition: all 0.3s ease;
                font-family: 'Inter', sans-serif;
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #2774AE;
                box-shadow: 0 0 0 3px rgba(39, 116, 174, 0.1);
            }
            
            input[type="submit"] { 
                background: linear-gradient(135deg, #2774AE 0%, #1e5b8c 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 1.1em;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600;
                width: 100%;
            }
            
            input[type="submit"]:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(39, 116, 174, 0.4);
            }
            
            .description {
                color: #4a5568;
                margin-bottom: 30px;
                font-size: 1.1em;
                line-height: 1.6;
            }
            
            .tagline {
                color: white;
                font-size: 2em;
                font-weight: 600;
                text-align: center;
                margin: 40px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            @media (max-width: 768px) {
                .features-container {
                    grid-template-columns: 1fr;
                }
                
                .feature-card {
                    margin-bottom: 20px;
                }
                
                h1 {
                    font-size: 2.5em;
                }
                
                .motto {
                    font-size: 1.4em;
                }
            }
        </style>
    </head>
    <body>
        <section class="hero">
            <div class="container">
                <h1>Sleuth</h1>
                <p class="motto">Find Your Future</p>
                <p class="description">
                    Discover clubs that match your interests and passions. Tell us what you're looking for, 
                    and we'll help you find the perfect UCLA clubs to join!
                </p>
                <div class="form-container">
                    <form action="/submit" method="post">
                        <input type="text" 
                               name="query" 
                               placeholder="Tell us a bit about your interests. Keep it short and sweet, and we'll help you focus on what matters most-- achieving your goals."
                               required>
                        <input type="submit" value="Find My Clubs">
                    </form>
                </div>
            </div>
            <a href="#features" class="scroll-indicator">
                <i class="fas fa-chevron-down"></i>
            </a>
        </section>
        
        <section id="features" class="features">
            <h2 class="tagline">Sleuth: Built for Students</h2>
            <div class="features-container">
                <div class="feature-card">
                    <i class="fas fa-compass feature-icon"></i>
                    <h3 class="feature-title">Smart Discovery</h3>
                    <p class="feature-description">
                        Our AI-powered system understands your interests and matches you with the perfect clubs.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-users feature-icon"></i>
                    <h3 class="feature-title">Community Focus</h3>
                    <p class="feature-description">
                        Connect with like-minded peers and find your place in UCLA's vibrant community.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-rocket feature-icon"></i>
                    <h3 class="feature-title">Future Ready</h3>
                    <p class="feature-description">
                        Develop skills, gain experience, and prepare for your future career through club involvement.
                    </p>
                </div>
            </div>
        </section>
    </body>
    </html>
    '''

# Load and process clubs
def load_and_process_clubs(file_path):
    try:
        # Get absolute path
        abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        print(f"Loading clubs from: {abs_path}")
        
        with open(abs_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        descriptions = []
        valid_items = []
        for item in data:
            if "description" in item and item["description"]:
                descriptions.append(item["description"].lower())
                valid_items.append(item)
        print(f"Successfully loaded {len(valid_items)} clubs")
        return descriptions, valid_items
    except Exception as e:
        print(f"Error loading clubs: {str(e)}")
        return [], []

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
    for idx in top_indices[0:top_k]:
        if similarities[idx] > 0:
            # Extract relevant activities and skills
            desc = valid_items[idx]['description'].lower()
            activities = []
            skills = set()
            
            # Look for activities in description
            if 'workshop' in desc:
                activities.append('Workshops')
            if 'project' in desc:
                activities.append('Project Work')
            if 'competition' in desc:
                activities.append('Competitions')
            if 'hackathon' in desc:
                activities.append('Hackathons')
            if 'research' in desc:
                activities.append('Research')
            if 'mentor' in desc:
                activities.append('Mentorship')
            if 'network' in desc:
                activities.append('Networking')
            
            # Look for skills
            if any(term in desc for term in ['program', 'coding', 'software']):
                skills.add('Programming')
            if 'data' in desc:
                skills.add('Data Analysis')
            if any(term in desc for term in ['ai', 'machine learning', 'artificial intelligence']):
                skills.add('AI/ML')
            if 'design' in desc:
                skills.add('Design')
            if 'leadership' in desc:
                skills.add('Leadership')
            if any(term in desc for term in ['team', 'collaboration']):
                skills.add('Teamwork')
            if 'research' in desc:
                skills.add('Research')
            if any(term in desc for term in ['pitch', 'present']):
                skills.add('Presentation')
            
            results.append((valid_items[idx], float(similarities[idx]), activities, list(skills)))
    return results

# Load clubs
club_descriptions, clubs = load_and_process_clubs("HOTH XII Orgs.json")
if not clubs:
    print("Warning: No clubs were loaded. Please check the file path and contents.")

# Endpoint to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    try:
        user_query = request.form.get('query', '')
        print('Received query:', user_query)

        if not clubs:
            return '''
            <html>
                <head>
                    <title>Error</title>
                    <style>
                        body { 
                            font-family: 'Inter', sans-serif;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            min-height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #2774AE 0%, #FFD100 100%);
                            padding: 20px;
                        }
                        .error-container {
                            background: white;
                            padding: 40px;
                            border-radius: 20px;
                            text-align: center;
                            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                            max-width: 600px;
                        }
                        h1 { color: #2774AE; margin-bottom: 20px; }
                        p { color: #4a5568; line-height: 1.6; margin-bottom: 20px; }
                        a {
                            display: inline-block;
                            background: #2774AE;
                            color: white;
                            padding: 12px 24px;
                            border-radius: 8px;
                            text-decoration: none;
                            transition: all 0.3s ease;
                        }
                        a:hover {
                            transform: translateY(-2px);
                            box-shadow: 0 5px 15px rgba(39, 116, 174, 0.4);
                        }
                    </style>
                </head>
                <body>
                    <div class="error-container">
                        <h1>Oops! Something went wrong</h1>
                        <p>We couldn't load the club data. Please try again later.</p>
                        <a href="/">Back to Home</a>
                    </div>
                </body>
            </html>
            '''

        # Get recommendations
        results = get_recommendations(club_descriptions, clubs, user_query, top_k=5)
        
        if not results:
            return '''
            <html>
                <head>
                    <title>No Results</title>
                    <style>
                        body { 
                            font-family: 'Inter', sans-serif;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            min-height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #2774AE 0%, #FFD100 100%);
                            padding: 20px;
                        }
                        .error-container {
                            background: white;
                            padding: 40px;
                            border-radius: 20px;
                            text-align: center;
                            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                            max-width: 600px;
                        }
                        h1 { color: #2774AE; margin-bottom: 20px; }
                        p { color: #4a5568; line-height: 1.6; margin-bottom: 20px; }
                        a {
                            display: inline-block;
                            background: #2774AE;
                            color: white;
                            padding: 12px 24px;
                            border-radius: 8px;
                            text-decoration: none;
                            transition: all 0.3s ease;
                        }
                        a:hover {
                            transform: translateY(-2px);
                            box-shadow: 0 5px 15px rgba(39, 116, 174, 0.4);
                        }
                    </style>
                </head>
                <body>
                    <div class="error-container">
                        <h1>No Matching Clubs Found</h1>
                        <p>We couldn't find any clubs matching your interests. Try broadening your search or using different keywords.</p>
                        <a href="/">Try Again</a>
                    </div>
                </body>
            </html>
            '''
        
        # Create HTML response
        html_response = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sleuth - Club Recommendations</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { 
                    margin: 0; 
                    padding: 0; 
                    box-sizing: border-box;
                    font-family: 'Inter', sans-serif;
                }
                
                body { 
                    background: linear-gradient(135deg, #2774AE 0%, #FFD100 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                
                .back-button { 
                    margin-bottom: 20px;
                }
                
                .back-button a { 
                    color: white;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    font-weight: 500;
                    font-size: 1.1em;
                    transition: all 0.3s ease;
                    background: rgba(39, 116, 174, 0.2);
                    padding: 10px 20px;
                    border-radius: 8px;
                    backdrop-filter: blur(5px);
                }
                
                .back-button a:hover { 
                    transform: translateX(-5px);
                    background: rgba(39, 116, 174, 0.3);
                }
                
                h1 { 
                    text-align: center; 
                    color: white;
                    margin-bottom: 30px;
                    font-size: 2.5em;
                    font-weight: 700;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .club { 
                    background: rgba(255, 255, 255, 0.95);
                    margin-bottom: 30px;
                    padding: 30px;
                    border-radius: 20px;
                    position: relative;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    backdrop-filter: blur(10px);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                }
                
                .club h3 {
                    color: #2774AE;
                    font-size: 1.5em;
                    margin-bottom: 15px;
                    font-weight: 700;
                }
                
                .club-content {
                    display: grid;
                    grid-template-columns: 200px 2fr 1fr;
                    gap: 30px;
                    align-items: start;
                }
                
                .club-image {
                    width: 200px;
                    height: 200px;
                    border-radius: 10px;
                    overflow: hidden;
                    position: relative;
                    background-size: cover;
                    background-position: center;
                    margin-right: 20px;
                    flex-shrink: 0;
                }
                
                .club-image-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(39, 116, 174, 0.7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .club-image:hover .club-image-overlay {
                    opacity: 1;
                }
                
                .club-image-overlay i {
                    color: white;
                    font-size: 3rem;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                }
                
                .club-main p {
                    color: #4a5568;
                    line-height: 1.6;
                    margin-bottom: 20px;
                    font-size: 1.1em;
                }
                
                .contact {
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 20px;
                    border: 1px solid #e2e8f0;
                }
                
                .contact p { 
                    margin: 10px 0;
                    display: flex;
                    align-items: center;
                }
                
                .contact-label {
                    color: #64748b;
                    width: 100px;
                    font-weight: 600;
                }
                
                .contact a {
                    color: #2774AE;
                    text-decoration: none;
                    transition: all 0.3s ease;
                }
                
                .contact a:hover {
                    color: #1e5b8c;
                }
                
                .club-match {
                    background: #f8fafc;
                    padding: 25px;
                    border-radius: 12px;
                    border: 1px solid #e2e8f0;
                }
                
                .match-title {
                    font-weight: 700;
                    margin-bottom: 20px;
                    color: #2774AE;
                    font-size: 1.2em;
                }
                
                .match-section {
                    margin-bottom: 25px;
                }
                
                .match-section h4 {
                    color: #4a5568;
                    margin-bottom: 12px;
                    font-weight: 600;
                }
                
                .tag-list {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }
                
                .tag {
                    background: white;
                    padding: 6px 12px;
                    border-radius: 8px;
                    font-size: 0.9em;
                    color: #2774AE;
                    font-weight: 500;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    border: 1px solid #e2e8f0;
                }
                
                @media (max-width: 1024px) {
                    .club-content {
                        grid-template-columns: 1fr 1fr;
                    }
                    
                    .club-image {
                        display: none;
                    }
                }
                
                @media (max-width: 768px) {
                    .club-content {
                        grid-template-columns: 1fr;
                    }
                    
                    .club {
                        padding: 20px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="back-button">
                    <a href="/">← Back to Search</a>
                </div>
                <h1>Recommended Clubs</h1>
            '''
        
        # Add clubs to the response
        for idx, (club, score, activities, skills) in enumerate(results, 1):
            # Extract Instagram handle from URL
            instagram = club.get('instagram', '')
            if instagram and 'instagram.com/' in instagram.lower():
                parts = instagram.split('instagram.com/')[1].split('?')[0].split('/')[0]
                instagram_handle = f"@{parts}"
                instagram_link = f"https://www.instagram.com/{parts}"
            else:
                instagram_handle = 'N/A'
                instagram_link = '#'

            # Clean email format
            email = club.get('email', 'N/A')
            if isinstance(email, list):
                email = email[0] if email else 'N/A'
            email = email.strip('[]<> ')

            # Generate club image and add to response
            club_text = (club['name'] + ' ' + club['description']).lower()
            
            # Map categories to icons and images
            category_map = {
                'engineering': {
                    'icon': 'fa-microchip',
                    'image': 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0'
                },
                'business': {
                    'icon': 'fa-briefcase',
                    'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40'
                },
                'tech': {
                    'icon': 'fa-laptop-code',
                    'image': 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0'
                },
                'science': {
                    'icon': 'fa-flask',
                    'image': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d'
                },
                'art': {
                    'icon': 'fa-palette',
                    'image': 'https://images.unsplash.com/photo-1452860606245-08befc0ff44b'
                },
                'music': {
                    'icon': 'fa-music',
                    'image': 'https://images.unsplash.com/photo-1511379938547-c1f69419868d'
                },
                'health': {
                    'icon': 'fa-heart',
                    'image': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528'
                },
                'culture': {
                    'icon': 'fa-globe',
                    'image': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644'
                },
                'service': {
                    'icon': 'fa-hands-helping',
                    'image': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a'
                }
            }
            
            # Find matching category and add club HTML
            matched_category = None
            for category, info in category_map.items():
                if category in club_text:
                    matched_category = info
                    break
            
            if not matched_category:
                matched_category = {
                    'icon': 'fa-users',
                    'image': 'https://images.unsplash.com/photo-1523580494863-6f3031224c94'
                }

            html_response += f'''
            <div class="club">
                <div class="club-content">
                    <div class="club-image" style="background-image: url('{matched_category["image"]}?auto=format&fit=crop&w=400&q=80');">
                        <div class="club-image-overlay">
                            <i class="fas {matched_category["icon"]}"></i>
                        </div>
                    </div>
                    <div class="club-main">
                        <h3>{club['name']}</h3>
                        <p>{club['description']}</p>
                        <div class="contact">
                            <p><strong>Contact & Links</strong></p>
                            <p>
                                <span class="contact-label">Email:</span>
                                <a href="mailto:{email}">{email}</a>
                            </p>
                            <p>
                                <span class="contact-label">Instagram:</span>
                                <a href="{instagram_link}" target="_blank">{instagram_handle}</a>
                            </p>
                        </div>
                    </div>
                    <div class="club-match">
                        <div class="match-title">Club Insights</div>
                        
                        <div class="match-section">
                            <h4>Key Activities</h4>
                            <div class="tag-list">
                                {" ".join(f'<span class="tag">{activity}</span>' for activity in activities)}
                            </div>
                        </div>
                        
                        <div class="match-section">
                            <h4>Skills You'll Gain</h4>
                            <div class="tag-list">
                                {" ".join(f'<span class="tag">{skill}</span>' for skill in skills)}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            '''
        
        html_response += '''
            </div>
        </body>
        </html>
        '''
        
        return html_response
        
    except Exception as e:
        print(f"Error in submit: {str(e)}")
        return '''
        <html>
            <head>
                <title>Error</title>
                <style>
                    body { 
                        font-family: 'Inter', sans-serif;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #2774AE 0%, #FFD100 100%);
                        padding: 20px;
                    }
                    .error-container {
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        text-align: center;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                        max-width: 600px;
                    }
                    h1 { color: #2774AE; margin-bottom: 20px; }
                    p { color: #4a5568; line-height: 1.6; margin-bottom: 20px; }
                    a {
                        display: inline-block;
                        background: #2774AE;
                        color: white;
                        padding: 12px 24px;
                        border-radius: 8px;
                        text-decoration: none;
                        transition: all 0.3s ease;
                    }
                    a:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 5px 15px rgba(39, 116, 174, 0.4);
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <h1>Oops! Something went wrong</h1>
                    <p>An error occurred while processing your request. Please try again later.</p>
                    <a href="/">Back to Home</a>
                </div>
            </body>
        </html>
        '''

# Start the server
if __name__ == '__main__':
    app.run(port=5000)