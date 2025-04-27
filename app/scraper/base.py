from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import create_listing, update_listing, create_scraper_log
from app.db.session import AsyncSessionLocal

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """
    Base class for apartment listing scrapers
    """
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.start_time = None
        self.scraper_log = {
            "source": source_name,
            "listings_found": 0,
            "listings_added": 0,
            "listings_updated": 0,
            "success": False,
        }
    
    async def run(self):
        """
        Run the scraper and save results to database
        """
        self.start_time = datetime.utcnow()
        self.scraper_log["start_time"] = self.start_time
        
        try:
            # Get session
            async with AsyncSessionLocal() as session:
                # Scrape listings
                logger.info(f"Starting scraper for {self.source_name}")
                listings = await self.scrape()
                self.scraper_log["listings_found"] = len(listings)
                logger.info(f"Found {len(listings)} listings from {self.source_name}")
                
                # Process and save listings
                for listing_data in listings:
                    await self._process_listing(listing_data, session)
                
                # Log scraper run
                self.scraper_log["end_time"] = datetime.utcnow()
                self.scraper_log["success"] = True
                await create_scraper_log(self.scraper_log, session)
                
                logger.info(
                    f"Scraper for {self.source_name} completed. "
                    f"Added: {self.scraper_log['listings_added']}, "
                    f"Updated: {self.scraper_log['listings_updated']}"
                )
                
        except Exception as e:
            logger.error(f"Error running scraper for {self.source_name}: {str(e)}")
            
            # Log error
            self.scraper_log["end_time"] = datetime.utcnow()
            self.scraper_log["success"] = False
            self.scraper_log["error_message"] = str(e)
            
            async with AsyncSessionLocal() as session:
                await create_scraper_log(self.scraper_log, session)
    
    async def _process_listing(self, listing_data: Dict[str, Any], session: AsyncSession):
        """
        Process a listing and save to database
        """
        # Add source to listing data
        listing_data["source"] = self.source_name
        
        # Check if listing already exists by URL
        # TODO: Implement check for existing listings
        # For now, we'll assume all listings are new
        
        # Extract amenities if present
        amenities = listing_data.pop("amenities", None)
        
        # Create listing
        await create_listing(listing_data, amenities, session)
        self.scraper_log["listings_added"] += 1
    
    @abstractmethod
    async def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape apartment listings from source
        
        Returns:
            List of dictionaries with listing data
        """
        pass 