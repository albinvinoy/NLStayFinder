from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.nlp.processor import NLPProcessor
from app.db.crud import get_listings
from app.db.models import Listing

api_router = APIRouter()

@api_router.post("/search", response_model=Dict[str, Any])
async def search_apartments(query: str):
    """
    Process natural language query and return matching apartments
    """
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty",
        )
    
    # Process NLP query
    nlp_processor = NLPProcessor()
    search_params = nlp_processor.process_query(query)
    
    # Get listings from database
    listings = await get_listings(search_params)
    
    return {
        "query": query,
        "parameters": search_params,
        "results": listings,
        "count": len(listings)
    }

@api_router.get("/listings", response_model=List[Dict[str, Any]])
async def get_all_listings(
    city: str = None,
    min_bedrooms: int = None,
    max_price: float = None,
    limit: int = 10
):
    """
    Get apartment listings with optional filters
    """
    search_params = {
        "city": city,
        "min_bedrooms": min_bedrooms,
        "max_price": max_price
    }
    
    # Remove None values
    search_params = {k: v for k, v in search_params.items() if v is not None}
    
    # Get listings from database
    listings = await get_listings(search_params, limit=limit)
    
    return listings 