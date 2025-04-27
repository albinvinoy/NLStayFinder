from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Listing(Base):
    """
    Database model for apartment listings
    """
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    square_footage = Column(Float)
    address = Column(String)
    city = Column(String, nullable=False)
    state = Column(String)
    zip_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)
    source = Column(String)  # Which website the listing was scraped from
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    amenities = relationship("Amenity", back_populates="listing")
    
    def __repr__(self):
        return f"<Listing {self.title} - {self.city} - ${self.price}>"

class Amenity(Base):
    """
    Database model for apartment amenities
    """
    __tablename__ = "amenities"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    name = Column(String, nullable=False)
    
    listing = relationship("Listing", back_populates="amenities")
    
    def __repr__(self):
        return f"<Amenity {self.name}>"

class ScraperLog(Base):
    """
    Database model for tracking scraper runs
    """
    __tablename__ = "scraper_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # Which website was scraped
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    listings_found = Column(Integer, default=0)
    listings_added = Column(Integer, default=0)
    listings_updated = Column(Integer, default=0)
    success = Column(Boolean, default=False)
    error_message = Column(Text)
    
    def __repr__(self):
        return f"<ScraperLog {self.source} - {self.start_time}>" 