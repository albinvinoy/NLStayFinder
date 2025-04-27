import asyncio
import logging
import time
import re
import random
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from app.scraper.base import BaseScraper
from app.core.config import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ZillowScraper(BaseScraper):
    """
    Scraper for Zillow.com that adheres to robots.txt rules
    """
    
    def __init__(self):
        super().__init__("zillow.com")
        self.base_url = "https://www.zillow.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.robots_rules = settings.ZILLOW_ROBOTS_RULES
        self.crawl_delay = self.robots_rules["crawl_delay"]
        
    def is_url_allowed(self, url: str) -> bool:
        """
        Check if a URL is allowed according to robots.txt rules
        """
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        # Check if path is in allowed paths
        for allowed_path in self.robots_rules["allowed_paths"]:
            if path.startswith(allowed_path):
                # Now check if it's not in disallowed paths
                for disallowed_path in self.robots_rules["disallowed_paths"]:
                    if path.startswith(disallowed_path):
                        return False
                return True
        
        return False

    async def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape apartment listings from zillow.com
        """
        # Cities to search for rentals
        cities = [
            "san-francisco-ca",
            "los-angeles-ca", 
            "new-york-ny", 
            "chicago-il", 
            "seattle-wa"
        ]
        
        all_listings = []
        
        # Scrape each city
        for city in cities:
            # Construct URL that adheres to robots.txt rules
            city_url = f"{self.base_url}/homes/for_rent/{city}/"
            if not self.is_url_allowed(city_url):
                logger.warning(f"URL {city_url} is not allowed according to robots.txt rules. Skipping.")
                continue
                
            logger.info(f"Scraping rental listings for {city}")
            
            try:
                # Respect crawl delay
                await asyncio.sleep(self.crawl_delay)
                
                # Get city page
                response = requests.get(city_url, headers=self.headers)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find listing cards - Note: Actual selectors may vary based on Zillow's current HTML structure
                listing_cards = soup.select(".list-card")
                logger.info(f"Found {len(listing_cards)} listing cards for {city}")
                
                # Process each listing card
                for card in listing_cards:
                    try:
                        listing = self._parse_listing_card(card, city)
                        if listing:
                            all_listings.append(listing)
                    except Exception as e:
                        logger.error(f"Error parsing listing: {str(e)}")
                    
                    # Small random delay between processing items
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                logger.error(f"Error scraping {city_url}: {str(e)}")
        
        return all_listings
    
    def _parse_listing_card(self, card, city: str) -> Dict[str, Any]:
        """
        Parse a listing card from zillow.com
        
        Note: These selectors may need to be updated based on Zillow's actual HTML structure
        """
        # Extract listing URL
        url_tag = card.select_one(".list-card-link")
        if not url_tag:
            return None
        
        url = url_tag.get("href")
        if not url:
            return None
        
        # Make sure URL is absolute and check if it's allowed
        if not url.startswith("http"):
            url = urljoin(self.base_url, url)
            
        if not self.is_url_allowed(url):
            logger.warning(f"URL {url} is not allowed according to robots.txt rules. Skipping.")
            return None
        
        # Extract title
        title = url_tag.get_text().strip() if url_tag.get_text() else "Apartment for Rent"
        
        # Extract price
        price_tag = card.select_one(".list-card-price")
        price = 0
        if price_tag:
            price_text = price_tag.get_text().strip()
            # Extract numeric value from price string
            price_match = re.search(r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", price_text)
            if price_match:
                price = float(price_match.group(1).replace(",", ""))
        
        # Extract address
        address_tag = card.select_one(".list-card-addr")
        address = address_tag.get_text().strip() if address_tag else ""
        
        # Extract details (beds, baths, sqft)
        details_tag = card.select_one(".list-card-details")
        bedrooms = 0
        bathrooms = 0
        square_footage = 0
        
        if details_tag:
            details_text = details_tag.get_text().strip()
            
            # Extract bedrooms
            bed_match = re.search(r"(\d+)\s*bd", details_text, re.IGNORECASE)
            if bed_match:
                bedrooms = int(bed_match.group(1))
            
            # Extract bathrooms
            bath_match = re.search(r"(\d+(?:\.\d+)?)\s*ba", details_text, re.IGNORECASE)
            if bath_match:
                bathrooms = float(bath_match.group(1))
            
            # Extract square footage
            sqft_match = re.search(r"(\d+(?:,\d{3})*)\s*sqft", details_text, re.IGNORECASE)
            if sqft_match:
                square_footage = float(sqft_match.group(1).replace(",", ""))
        
        # Extract image URL
        image_tag = card.select_one(".list-card-img")
        image_url = ""
        if image_tag:
            if image_tag.get("src"):
                image_url = image_tag.get("src")
            elif image_tag.get("data-src"):
                image_url = image_tag.get("data-src")
        
        # Parse location from city string
        city_parts = city.split("-")
        city_name = " ".join(city_parts[:-1]).title()
        state = city_parts[-1].upper() if len(city_parts) > 1 else ""
        
        # Create listing data
        listing_data = {
            "title": title,
            "url": url,
            "price": price,
            "address": address,
            "city": city_name,
            "state": state,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "square_footage": square_footage,
            "image_url": image_url,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_available": True
        }
        
        return listing_data 