import logging

import requests

from ai_scraper.llm_backend import ScraperGeneratorBase


logger = logging.getLogger(__name__)


class OpenAIScraper(ScraperGeneratorBase):
    """OpenAILLM 
    
    Class to interact with the gpt3.5 turbo api.
    
    Args:
        api_key (str): ChatGPT API key
    """
    def __init__(self, api_key):
        self.api_key = api_key
    
    def generate_scraper(self):
        pass