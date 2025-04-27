"""
DEPRECATED: This scraper is no longer used. 
The application now exclusively uses the ZillowScraper to adhere to specific robots.txt rules.
See app/scraper/zillow_scraper.py for the current implementation.
"""

import asyncio
import logging
from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime

from app.scraper.base import BaseScraper

# Set up logging
logger = logging.getLogger(__name__)

class ApartmentsScraper(BaseScraper):
    """
    DEPRECATED: Scraper for apartments.com
    This class is no longer used by the application.
    """
    
    def __init__(self):
        super().__init__("apartments.com")
        self.base_url = "https://www.apartments.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
    
    async def scrape(self) -> List[Dict[str, Any]]:
        """
        DEPRECATED: Scrape apartment listings from apartments.com
        This method is no longer used by the application.
        """
        logger.warning("The ApartmentsScraper is deprecated and should not be used. Use ZillowScraper instead.")
        return []
    
    def _parse_listing_card(self, card, city: str) -> Dict[str, Any]:
        """
        DEPRECATED: Parse a listing card from apartments.com
        This method is no longer used by the application.
        """
        logger.warning("The ApartmentsScraper is deprecated and should not be used. Use ZillowScraper instead.")
        return None 