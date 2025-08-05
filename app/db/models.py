from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class PropertyType(enum.Enum):
    """Property type enumeration"""
    APARTMENT = "apartment"
    HOUSE = "house"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    STUDIO = "studio"
    LOFT = "loft"
    DUPLEX = "duplex"
    PENTHOUSE = "penthouse"
    VILLA = "villa"

class ListingStatus(enum.Enum):
    """Listing status enumeration"""
    AVAILABLE = "available"
    RENTED = "rented"
    PENDING = "pending"
    OFF_MARKET = "off_market"

class Listing(Base):
    """
    Comprehensive database model for real estate listings
    """
    __tablename__ = "listings"

    # Basic Information
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(500), nullable=False, unique=True)
    
    # Property Details
    property_type = Column(Enum(PropertyType), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    price_per_sqft = Column(Float)
    bedrooms = Column(Integer, index=True)
    bathrooms = Column(Float, index=True)
    square_footage = Column(Float, index=True)
    lot_size = Column(Float)  # For houses
    year_built = Column(Integer)
    
    # Location Information
    address = Column(String(255), index=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    zip_code = Column(String(20), index=True)
    neighborhood = Column(String(100), index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    
    # Property Features
    parking_spaces = Column(Integer)
    garage_spaces = Column(Integer)
    has_garage = Column(Boolean, default=False)
    has_parking = Column(Boolean, default=False)
    has_balcony = Column(Boolean, default=False)
    has_pool = Column(Boolean, default=False)
    has_gym = Column(Boolean, default=False)
    has_laundry = Column(Boolean, default=False)
    has_dishwasher = Column(Boolean, default=False)
    has_air_conditioning = Column(Boolean, default=False)
    has_heating = Column(Boolean, default=False)
    is_furnished = Column(Boolean, default=False)
    allows_pets = Column(Boolean, default=False)
    allows_smoking = Column(Boolean, default=False)
    
    # Lease Information
    lease_term = Column(String(50))  # "12 months", "month-to-month", etc.
    available_date = Column(Date)
    application_fee = Column(Float)
    security_deposit = Column(Float)
    utilities_included = Column(Boolean, default=False)
    
    # Neighborhood & School Information
    school_district = Column(String(100))
    elementary_school_rating = Column(Float)
    middle_school_rating = Column(Float)
    high_school_rating = Column(Float)
    walk_score = Column(Integer)
    transit_score = Column(Integer)
    bike_score = Column(Integer)
    crime_rate = Column(Float)
    
    # Market Information
    days_on_market = Column(Integer)
    price_history = Column(Text)  # JSON string of price changes
    market_trend = Column(String(50))  # "increasing", "decreasing", "stable"
    
    # Media & Images
    image_url = Column(String(500))
    image_urls = Column(Text)  # JSON array of image URLs
    virtual_tour_url = Column(String(500))
    
    # Source & Tracking
    source = Column(String(100), index=True)  # Website source
    listing_id_external = Column(String(100), index=True)  # External listing ID
    status = Column(Enum(ListingStatus), default=ListingStatus.AVAILABLE, index=True)
    is_available = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    last_seen = Column(DateTime, default=datetime.utcnow)  # Last time scraped
    
    # Search Optimization
    search_keywords = Column(Text)  # Keywords for full-text search
    price_range = Column(String(50))  # "1000-2000", "2000-3000", etc.
    bedroom_range = Column(String(20))  # "1-2", "3+", etc.
    
    # Relationships
    amenities = relationship("Amenity", back_populates="listing", cascade="all, delete-orphan")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Listing {self.title} - {self.city} - ${self.price}>"

class Amenity(Base):
    """
    Database model for property amenities
    """
    __tablename__ = "amenities"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(50))  # "indoor", "outdoor", "community", "utilities"
    
    listing = relationship("Listing", back_populates="amenities")
    
    def __repr__(self):
        return f"<Amenity {self.name}>"

class ListingImage(Base):
    """
    Database model for listing images
    """
    __tablename__ = "listing_images"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"))
    url = Column(String(500), nullable=False)
    caption = Column(String(255))
    is_primary = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)
    
    listing = relationship("Listing", back_populates="images")
    
    def __repr__(self):
        return f"<ListingImage {self.url}>"

class Neighborhood(Base):
    """
    Database model for neighborhood information
    """
    __tablename__ = "neighborhoods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    
    # Demographics
    population = Column(Integer)
    median_age = Column(Float)
    median_income = Column(Float)
    
    # Ratings
    safety_rating = Column(Float)
    walkability_rating = Column(Float)
    transit_rating = Column(Float)
    
    # Coordinates
    latitude = Column(Float)
    longitude = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Neighborhood {self.name} - {self.city}, {self.state}>"

class UserSearch(Base):
    """
    Database model for tracking user searches
    """
    __tablename__ = "user_searches"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    user_id = Column(String(100), index=True)  # If user is logged in
    
    # Search criteria
    city = Column(String(100), index=True)
    state = Column(String(50), index=True)
    min_price = Column(Float)
    max_price = Column(Float)
    min_bedrooms = Column(Integer)
    max_bedrooms = Column(Integer)
    property_type = Column(Enum(PropertyType))
    search_query = Column(Text)  # Raw search query
    
    # Results
    results_count = Column(Integer)
    search_time_ms = Column(Integer)  # How long the search took
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<UserSearch {self.city} - {self.min_price}-{self.max_price}>"

class ScraperLog(Base):
    """
    Database model for tracking scraper runs
    """
    __tablename__ = "scraper_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False, index=True)
    start_time = Column(DateTime, default=datetime.utcnow, index=True)
    end_time = Column(DateTime)
    duration_seconds = Column(Float)
    
    # Results
    listings_found = Column(Integer, default=0)
    listings_added = Column(Integer, default=0)
    listings_updated = Column(Integer, default=0)
    listings_removed = Column(Integer, default=0)
    
    # Status
    success = Column(Boolean, default=False)
    error_message = Column(Text)
    warnings = Column(Text)  # JSON array of warnings
    
    # Performance
    requests_made = Column(Integer, default=0)
    requests_failed = Column(Integer, default=0)
    avg_response_time = Column(Float)
    
    def __repr__(self):
        return f"<ScraperLog {self.source} - {self.start_time}>" 