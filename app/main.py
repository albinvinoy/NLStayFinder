import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from flask import Flask, render_template, request, jsonify
import uvicorn
from dotenv import load_dotenv

# Load environment variables (optional)
try:
    load_dotenv()
except Exception:
    pass  # Continue even if .env is not found

# Initialize FastAPI
app = FastAPI(
    title="NLStayFinder",
    description="NLP-based apartment finder application",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize Flask app for front-end
flask_app = Flask(__name__, 
                 template_folder="templates",
                 static_folder="static")

@flask_app.route("/")
def home():
    return render_template("index.html")

@flask_app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Return mock data (no real processing)
    mock_results = {
        "query": query,
        "parameters": {
            "city": "San Francisco",
            "min_bedrooms": 1,
            "max_price": 3000
        },
        "results": [],
        "count": 0
    }
    
    return jsonify(mock_results)

if __name__ == "__main__":
    # Run Flask app directly for simplicity
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port, debug=True) 