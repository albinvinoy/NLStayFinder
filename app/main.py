import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from flask import Flask, render_template, request, jsonify
import uvicorn
from dotenv import load_dotenv

from app.core.config import settings
from app.api.routes import api_router
from app.nlp.processor import NLPProcessor

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NLP-based apartment finder application",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)

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
    
    # Process the NLP query
    nlp_processor = NLPProcessor()
    results = nlp_processor.process_query(query)
    
    return jsonify(results)

if __name__ == "__main__":
    # Run FastAPI with uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 