import sys
import os
from pathlib import Path
from datetime import datetime, date
import json

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Listing, Amenity, ListingImage, Neighborhood, UserSearch, ScraperLog
from app.db.models import PropertyType, ListingStatus
from app.core.config import settings

def check_table_exists(engine, table_name):
    """Check if a table exists in the database"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def create_tables():
    """
    Create all database tables if they don't exist
    """
    print("Connecting to database...")
    
    # Create engine with SQLite-specific settings
    if settings.is_sqlite:
        engine = create_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            connect_args={"check_same_thread": False}
        )
    else:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    # Check if tables already exist
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if existing_tables:
        print(f"Found existing tables: {existing_tables}")
        response = input("Tables already exist. Do you want to recreate them? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing tables.")
            return
        else:
            print("Dropping existing tables...")
            Base.metadata.drop_all(engine)
    
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    
    # Verify tables were created
    inspector = inspect(engine)
    created_tables = inspector.get_table_names()
    print(f"Successfully created tables: {created_tables}")
    
    return engine

def seed_sample_data(engine):
    """
    Add sample real estate data for testing
    """
    print("Adding sample data...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as session:
        # Sample neighborhoods
        neighborhoods = [
            {
                "name": "Downtown Amsterdam",
                "city": "Amsterdam",
                "state": "NH",
                "description": "Vibrant downtown area with shopping, restaurants, and nightlife",
                "population": 15000,
                "median_age": 32.5,
                "median_income": 75000,
                "safety_rating": 8.5,
                "walkability_rating": 9.2,
                "transit_rating": 9.0,
                "latitude": 42.9896,
                "longitude": -71.4654
            },
            {
                "name": "University District",
                "city": "Amsterdam",
                "state": "NH",
                "description": "College town area near the university campus",
                "population": 8000,
                "median_age": 24.5,
                "median_income": 45000,
                "safety_rating": 7.8,
                "walkability_rating": 8.5,
                "transit_rating": 8.2,
                "latitude": 42.9876,
                "longitude": -71.4632
            }
        ]
        
        for neighborhood_data in neighborhoods:
            neighborhood = Neighborhood(**neighborhood_data)
            session.add(neighborhood)
        
        session.flush()  # Get neighborhood IDs
        
        # Sample listings
        sample_listings = [
            {
                "title": "Modern 2BR Apartment in Downtown",
                "description": "Beautiful modern apartment with great amenities, hardwood floors, and updated kitchen. Perfect for young professionals.",
                "url": "https://example.com/listing1",
                "property_type": PropertyType.APARTMENT,
                "price": 2500.0,
                "price_per_sqft": 2.08,
                "bedrooms": 2,
                "bathrooms": 2.0,
                "square_footage": 1200.0,
                "year_built": 2015,
                "address": "123 Main St",
                "city": "Amsterdam",
                "state": "NH",
                "zip_code": "03031",
                "neighborhood": "Downtown Amsterdam",
                "latitude": 42.9896,
                "longitude": -71.4654,
                "parking_spaces": 1,
                "has_garage": True,
                "has_parking": True,
                "has_balcony": True,
                "has_gym": True,
                "has_laundry": True,
                "has_dishwasher": True,
                "has_air_conditioning": True,
                "has_heating": True,
                "is_furnished": False,
                "allows_pets": True,
                "allows_smoking": False,
                "lease_term": "12 months",
                "available_date": date(2024, 1, 15),
                "application_fee": 50.0,
                "security_deposit": 2500.0,
                "utilities_included": False,
                "school_district": "Amsterdam School District",
                "elementary_school_rating": 8.5,
                "middle_school_rating": 8.2,
                "high_school_rating": 8.8,
                "walk_score": 92,
                "transit_score": 88,
                "bike_score": 85,
                "crime_rate": 2.1,
                "days_on_market": 5,
                "market_trend": "increasing",
                "image_url": "https://example.com/image1.jpg",
                "image_urls": json.dumps([
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg",
                    "https://example.com/image3.jpg"
                ]),
                "source": "sample",
                "listing_id_external": "SAMPLE001",
                "status": ListingStatus.AVAILABLE,
                "is_available": True,
                "search_keywords": "modern apartment downtown amenities hardwood floors updated kitchen",
                "price_range": "2000-3000",
                "bedroom_range": "2"
            },
            {
                "title": "Cozy 1BR Studio Near University",
                "description": "Perfect studio apartment for students or young professionals. Close to campus and downtown.",
                "url": "https://example.com/listing2",
                "property_type": PropertyType.STUDIO,
                "price": 1800.0,
                "price_per_sqft": 2.25,
                "bedrooms": 1,
                "bathrooms": 1.0,
                "square_footage": 800.0,
                "year_built": 2010,
                "address": "456 College Ave",
                "city": "Amsterdam",
                "state": "NH",
                "zip_code": "03031",
                "neighborhood": "University District",
                "latitude": 42.9876,
                "longitude": -71.4632,
                "parking_spaces": 0,
                "has_garage": False,
                "has_parking": False,
                "has_balcony": False,
                "has_gym": False,
                "has_laundry": True,
                "has_dishwasher": True,
                "has_air_conditioning": True,
                "has_heating": True,
                "is_furnished": True,
                "allows_pets": False,
                "allows_smoking": False,
                "lease_term": "9 months",
                "available_date": date(2024, 1, 1),
                "application_fee": 35.0,
                "security_deposit": 1800.0,
                "utilities_included": True,
                "school_district": "Amsterdam School District",
                "elementary_school_rating": 8.0,
                "middle_school_rating": 7.8,
                "high_school_rating": 8.5,
                "walk_score": 85,
                "transit_score": 82,
                "bike_score": 88,
                "crime_rate": 2.8,
                "days_on_market": 12,
                "market_trend": "stable",
                "image_url": "https://example.com/image2.jpg",
                "image_urls": json.dumps([
                    "https://example.com/image2.jpg",
                    "https://example.com/image4.jpg"
                ]),
                "source": "sample",
                "listing_id_external": "SAMPLE002",
                "status": ListingStatus.AVAILABLE,
                "is_available": True,
                "search_keywords": "cozy studio university campus downtown furnished",
                "price_range": "1500-2000",
                "bedroom_range": "1"
            },
            {
                "title": "Luxury 3BR Townhouse with Garage",
                "description": "Spacious townhouse with attached garage, modern appliances, and private backyard. Perfect for families.",
                "url": "https://example.com/listing3",
                "property_type": PropertyType.TOWNHOUSE,
                "price": 3200.0,
                "price_per_sqft": 1.78,
                "bedrooms": 3,
                "bathrooms": 2.5,
                "square_footage": 1800.0,
                "lot_size": 2500.0,
                "year_built": 2018,
                "address": "789 Oak St",
                "city": "Amsterdam",
                "state": "NH",
                "zip_code": "03031",
                "neighborhood": "Downtown Amsterdam",
                "latitude": 42.9901,
                "longitude": -71.4648,
                "parking_spaces": 2,
                "garage_spaces": 1,
                "has_garage": True,
                "has_parking": True,
                "has_balcony": False,
                "has_pool": False,
                "has_gym": False,
                "has_laundry": True,
                "has_dishwasher": True,
                "has_air_conditioning": True,
                "has_heating": True,
                "is_furnished": False,
                "allows_pets": True,
                "allows_smoking": False,
                "lease_term": "12 months",
                "available_date": date(2024, 2, 1),
                "application_fee": 75.0,
                "security_deposit": 3200.0,
                "utilities_included": False,
                "school_district": "Amsterdam School District",
                "elementary_school_rating": 9.0,
                "middle_school_rating": 8.8,
                "high_school_rating": 9.2,
                "walk_score": 78,
                "transit_score": 75,
                "bike_score": 82,
                "crime_rate": 1.8,
                "days_on_market": 3,
                "market_trend": "increasing",
                "image_url": "https://example.com/image3.jpg",
                "image_urls": json.dumps([
                    "https://example.com/image3.jpg",
                    "https://example.com/image5.jpg",
                    "https://example.com/image6.jpg",
                    "https://example.com/image7.jpg"
                ]),
                "source": "sample",
                "listing_id_external": "SAMPLE003",
                "status": ListingStatus.AVAILABLE,
                "is_available": True,
                "search_keywords": "luxury townhouse garage modern appliances backyard family",
                "price_range": "3000-3500",
                "bedroom_range": "3+"
            }
        ]
        
        for listing_data in sample_listings:
            listing = Listing(**listing_data)
            session.add(listing)
            session.flush()  # Get the listing ID
            
            # Add amenities based on property type
            if listing.property_type == PropertyType.APARTMENT:
                amenities = ["Hardwood Floors", "Updated Kitchen", "Balcony", "Gym Access", "Laundry Room"]
            elif listing.property_type == PropertyType.STUDIO:
                amenities = ["Furnished", "Utilities Included", "Laundry Room", "High-Speed Internet"]
            else:  # Townhouse
                amenities = ["Attached Garage", "Private Backyard", "Modern Appliances", "Laundry Room", "Storage Space"]
            
            for amenity_name in amenities:
                amenity = Amenity(
                    listing_id=listing.id, 
                    name=amenity_name,
                    category="indoor" if "Kitchen" in amenity_name or "Laundry" in amenity_name else "outdoor"
                )
                session.add(amenity)
            
            # Add sample images
            image_urls = json.loads(listing.image_urls) if listing.image_urls else [listing.image_url]
            for i, image_url in enumerate(image_urls):
                image = ListingImage(
                    listing_id=listing.id,
                    url=image_url,
                    caption=f"Image {i+1} for {listing.title}",
                    is_primary=(i == 0),
                    order_index=i
                )
                session.add(image)
        
        # Add sample user search
        user_search = UserSearch(
            session_id="sample_session_123",
            city="Amsterdam",
            state="NH",
            min_price=1500.0,
            max_price=3000.0,
            min_bedrooms=1,
            max_bedrooms=3,
            property_type=PropertyType.APARTMENT,
            search_query="apartment in Amsterdam under $3000",
            results_count=3,
            search_time_ms=245
        )
        session.add(user_search)
        
        # Add sample scraper log
        scraper_log = ScraperLog(
            source="sample_scraper",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_seconds=45.2,
            listings_found=3,
            listings_added=3,
            listings_updated=0,
            listings_removed=0,
            success=True,
            requests_made=10,
            requests_failed=0,
            avg_response_time=1.2
        )
        session.add(scraper_log)
        
        session.commit()
        print("Sample data added successfully!")

def main():
    """Main function to create tables and seed data"""
    print("=== NLStayFinder Database Setup ===")
    print(f"Database: {settings.SQLALCHEMY_DATABASE_URI}")
    
    try:
        # Create tables
        engine = create_tables()
        
        # Ask if user wants sample data
        response = input("\nDo you want to add sample data? (Y/n): ")
        if response.lower() != 'n':
            seed_sample_data(engine)
        
        print("\n✅ Database setup complete!")
        print(f"Database file: {settings.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')}")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 