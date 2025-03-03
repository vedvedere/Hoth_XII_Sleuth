# Sleuth - UCLA Club Recommendation System

A smart club recommendation system that helps UCLA students find clubs matching their interests using AI-powered matching.

## Features

- Natural language query processing
- Smart club matching based on interests
- Beautiful, responsive UI
- Club categorization and skill mapping
- Contact information and social media links

## Local Development Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
python recommend.py
```

The application will be available at `http://localhost:5000`

## Deployment

### Heroku Deployment

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Push to Heroku:
```bash
git push heroku main
```

### Manual Deployment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run with Gunicorn:
```bash
gunicorn recommend:app
```

## Data

The application uses the `HOTH XII Orgs.json` file for club data. Make sure this file is present in the root directory.

## Environment Variables

No environment variables are required for basic functionality.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
