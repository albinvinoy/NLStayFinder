# NLStayFinder

NLStayFinder is a natural language processing (NLP) based application that helps users find apartments by processing natural language queries like "Find me apartments in San Francisco. At least 1 bed 1 bath around $3000".

## Features

- Natural language processing for apartment search queries
- Real-time apartment listing search based on user criteria
- Automated web scraping to keep the database updated
- Simple and intuitive chat interface

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Flask with Jinja templates
- **Database**: PostgreSQL
- **NLP**: spaCy, NLTK
- **Web Scraping**: BeautifulSoup4, Selenium, Scrapy
- **Deployment**: AWS (EC2, RDS, Lambda)

## Project Structure

```
NLStayFinder/
├── app/                    # Main application directory
│   ├── api/                # API endpoints
│   ├── core/               # Core functionality
│   ├── db/                 # Database models and operations
│   ├── nlp/                # NLP processing modules
│   ├── scraper/            # Web scraping modules
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   └── main.py             # Application entry point
├── config/                 # Configuration files
├── scripts/                # Utility scripts
├── tests/                  # Test modules
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── docker-compose.yml      # Docker Compose configuration
```

## Setup and Installation

1. Clone the repository
2. Create and activate virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env` file
5. Run the application: `python -m app.main`

## Deployment

Instructions for AWS deployment can be found in the `docs/deployment.md` file.

## License

This project is licensed under the terms of the included LICENSE file. 