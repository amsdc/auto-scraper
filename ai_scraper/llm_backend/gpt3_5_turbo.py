import requests

from ai_scraper import html_helpers

class OpenAILLM():
    """OpenAILLM 
    
    Class to interact with the gpt3.5 turbo api.
    
    Args:
        api_key (str): ChatGPT API key
    """
    def __init__(self, api_key):
        self.api_key = api_key
    
    def set_page(self, page):
        self.url = page
    
    def fetch_clean_html(self, user_agent="Atlanta/1.0"):
        print(requests.get(self.url, headers={"User-Agent": user_agent}).text)
        return html_helpers.preprocess_html(
            requests.get(self.url, headers={"User-Agent": user_agent}).text
            )
    
    def call_openai(self):
        pass