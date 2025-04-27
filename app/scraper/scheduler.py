import asyncio
import logging
import schedule
import time
from datetime import datetime
from typing import List

from app.core.config import settings
from app.scraper.zillow_scraper import ZillowScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ScraperScheduler:
    """
    Scheduler for running apartment listing scrapers periodically
    """
    
    def __init__(self):
        self.scrapers = [
            ZillowScraper(),  # Only using Zillow scraper
        ]
        self.interval_hours = settings.SCRAPER_INTERVAL_HOURS
        self.is_running = False
    
    def start(self):
        """
        Start the scheduler
        """
        logger.info(f"Starting Zillow scraper scheduler with interval of {self.interval_hours} hours")
        
        # Run scrapers once at startup
        self._run_scrapers()
        
        # Schedule regular runs
        schedule.every(self.interval_hours).hours.do(self._run_scrapers)
        
        self.is_running = True
        
        # Keep the scheduler running
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def stop(self):
        """
        Stop the scheduler
        """
        logger.info("Stopping Zillow scraper scheduler")
        self.is_running = False
    
    def _run_scrapers(self):
        """
        Run Zillow scraper
        """
        logger.info(f"Running Zillow scraper at {datetime.now()}")
        
        # Create and run a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run scraper
        for scraper in self.scrapers:
            try:
                loop.run_until_complete(scraper.run())
            except Exception as e:
                logger.error(f"Error running scraper {scraper.source_name}: {str(e)}")
        
        loop.close()
        
        logger.info("Zillow scraper completed")
        return True  # Return True to keep the schedule


# Function to start the scheduler in a separate thread
def start_scheduler_thread():
    """
    Start the Zillow scraper scheduler in a separate thread
    """
    import threading
    
    scheduler = ScraperScheduler()
    thread = threading.Thread(target=scheduler.start)
    thread.daemon = True
    thread.start()
    
    return scheduler, thread 