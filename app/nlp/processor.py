import spacy
import re
from typing import Dict, Any, List, Optional
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NLPProcessor:
    """
    NLP processor for apartment search queries
    """
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Download if not available
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Patterns for specific entities
        self.patterns = {
            "price": re.compile(r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+)(?:k)?", re.IGNORECASE),
            "bedrooms": re.compile(r"(\d+)(?:\s*(?:bed|bedroom|br)s?)", re.IGNORECASE),
            "bathrooms": re.compile(r"(\d+(?:\.\d+)?)(?:\s*(?:bath|bathroom|ba)s?)", re.IGNORECASE),
            "square_feet": re.compile(r"(\d+(?:,\d{3})*)(?:\s*(?:sq\.?\s*f(?:ee)?t|sf|sqft|ft2))", re.IGNORECASE),
        }
        
        # Common location phrases
        self.location_phrases = ["in", "near", "around", "close to"]
        
        # Known city names (can be extended with more cities)
        self.cities = [
            "san francisco", "los angeles", "new york", "chicago", "seattle", 
            "boston", "austin", "miami", "denver", "portland"
        ]
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query and extract search parameters
        """
        # Convert to lowercase for easier matching
        query = query.lower()
        
        # Process with spaCy
        doc = self.nlp(query)
        
        # Initialize parameters
        params = {
            "city": None,
            "min_bedrooms": None,
            "min_bathrooms": None,
            "min_price": None,
            "max_price": None
        }
        
        # Extract city
        for city in self.cities:
            if city in query:
                params["city"] = city.title()  # Convert to title case
                break
        
        # If city not found directly, check for location phrases
        if not params["city"]:
            for entity in doc.ents:
                if entity.label_ == "GPE":  # Geopolitical entity (city, state, country)
                    params["city"] = entity.text.title()
                    break
        
        # Extract bedrooms
        bedroom_matches = self.patterns["bedrooms"].findall(query)
        if bedroom_matches:
            params["min_bedrooms"] = int(bedroom_matches[0])
        
        # Extract bathrooms
        bathroom_matches = self.patterns["bathrooms"].findall(query)
        if bathroom_matches:
            params["min_bathrooms"] = float(bathroom_matches[0])
        
        # Extract price
        price_matches = self.patterns["price"].findall(query)
        if price_matches:
            # Check for price range
            if len(price_matches) >= 2:
                # Sort to determine min and max
                prices = sorted([self._convert_price(p) for p in price_matches])
                params["min_price"] = prices[0]
                params["max_price"] = prices[-1]
            else:
                # If only one price mentioned, assume it's max price
                price = self._convert_price(price_matches[0])
                
                # Check if query contains phrases indicating min or max
                if "at least" in query or "minimum" in query or "min" in query:
                    params["min_price"] = price
                else:
                    # Default to max price
                    params["max_price"] = price
        
        return params
    
    def _convert_price(self, price_str: str) -> float:
        """
        Convert price string to float
        """
        # Remove commas and dollar signs
        price_str = price_str.replace(",", "").replace("$", "")
        
        # Handle "k" suffix (thousands)
        if price_str.lower().endswith("k"):
            return float(price_str[:-1]) * 1000
        
        return float(price_str) 