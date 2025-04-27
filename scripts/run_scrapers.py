import asyncio
import sys
import os
import logging
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.scraper.zillow_scraper import ZillowScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def run_zillow_scraper():
    """
    Run the Zillow scraper
    """
    logger.info("Starting Zillow scraper")
    
    # Run Zillow scraper
    zillow_scraper = ZillowScraper()
    await zillow_scraper.run()
    
    logger.info("Zillow scraper completed")

if __name__ == "__main__":
    logger.info("Starting Zillow scraper script")
    
    # Create and run event loop
    loop = asyncio.get_event_loop()
    
    # Run Zillow scraper
    loop.run_until_complete(run_zillow_scraper())
    
    logger.info("Script completed") 