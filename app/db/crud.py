from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, and_
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.db.models import Listing, Amenity, ScraperLog

async def get_listings(
    filters: Dict[str, Any],
    session: AsyncSession = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get apartment listings with optional filters
    """
    query = select(Listing).where(Listing.is_available == True)
    
    # Apply filters
    if "city" in filters:
        query = query.where(Listing.city.ilike(f"%{filters['city']}%"))
    
    if "state" in filters:
        query = query.where(Listing.state == filters["state"])
    
    if "min_price" in filters:
        query = query.where(Listing.price >= filters["min_price"])
    
    if "max_price" in filters:
        query = query.where(Listing.price <= filters["max_price"])
    
    if "min_bedrooms" in filters:
        query = query.where(Listing.bedrooms >= filters["min_bedrooms"])
    
    if "min_bathrooms" in filters:
        query = query.where(Listing.bathrooms >= filters["min_bathrooms"])
    
    # Apply limit
    query = query.limit(limit)
    
    # Execute query
    result = await session.execute(query)
    listings = result.scalars().all()
    
    # Convert to dictionary
    return [
        {
            "id": listing.id,
            "title": listing.title,
            "description": listing.description,
            "url": listing.url,
            "price": listing.price,
            "bedrooms": listing.bedrooms,
            "bathrooms": listing.bathrooms,
            "square_footage": listing.square_footage,
            "address": listing.address,
            "city": listing.city,
            "state": listing.state,
            "zip_code": listing.zip_code,
            "image_url": listing.image_url,
            "source": listing.source,
            "created_at": listing.created_at.isoformat(),
            "updated_at": listing.updated_at.isoformat(),
        }
        for listing in listings
    ]

async def create_listing(
    listing_data: Dict[str, Any],
    amenities: Optional[List[str]] = None,
    session: AsyncSession = None
) -> Listing:
    """
    Create a new apartment listing
    """
    listing = Listing(**listing_data)
    session.add(listing)
    await session.flush()
    
    # Add amenities if provided
    if amenities:
        for amenity_name in amenities:
            amenity = Amenity(listing_id=listing.id, name=amenity_name)
            session.add(amenity)
    
    await session.commit()
    await session.refresh(listing)
    return listing

async def update_listing(
    listing_id: int,
    listing_data: Dict[str, Any],
    session: AsyncSession = None
) -> bool:
    """
    Update an existing apartment listing
    """
    stmt = (
        update(Listing)
        .where(Listing.id == listing_id)
        .values(**listing_data)
        .values(updated_at=datetime.utcnow())
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0

async def create_scraper_log(
    log_data: Dict[str, Any],
    session: AsyncSession = None
) -> ScraperLog:
    """
    Create a new scraper log entry
    """
    log = ScraperLog(**log_data)
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log 