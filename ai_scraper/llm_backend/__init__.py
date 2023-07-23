import logging
from abc import ABC, abstractmethod

import requests

from ai_scraper.llm_backend import html_helpers


logger = logging.getLogger(__name__)


class ScraperGeneratorBase(ABC):
    @abstractmethod
    def __init__(self):
        """__init__ 
        
        Initialise a scraper. Use an API key as args.
        """
        pass
    
    def set_page(self, page):
        self.url = page
    
    def fetch_clean_html(self, user_agent="Atlanta/1.0"):
        data = requests.get(self.url, headers={"User-Agent": user_agent}).text
        logger.debug(data)
        return html_helpers.preprocess_html(data)
    
    @abstractmethod
    def generate_scraper(self):
        pass