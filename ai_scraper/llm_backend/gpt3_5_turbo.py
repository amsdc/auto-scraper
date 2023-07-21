import logging
import requests
from ai_scraper.llm_backend import ScraperGeneratorBase
from typing import Optionl
from ai_scraper import html_helpers

logger = logging.getLogger(__name__)


class OpenAIScraper(ScraperGeneratorBase):
    """OpenAILLM 
    
    Class to interact with the gpt3.5 turbo api.
    
    Args:
        api_key (str): ChatGPT API key
    """
    def __init__(self, url):
        self.url = url
    
    def get_html(self):
        html_string = html_helpers.preprocess_html(self.url)
        self.html_string = html_string

    def generate_scraper(self):
        pass

    def suggest_fields(self,k:Optional[int] = 30000):
        input_template = {
            "spec_version": "1.0",
            "page_url": self.url,
            "page_html": str(self.html_string)[0:k],
        }
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            temperature = 0.0,
            messages =  [{"role": "system", "content": prompt_string}, {"role": "user", "content": str(input_template)}]
        )
            
        print(completion)
        text = completion['choices'][0]['message']['content']
        print(text)
        return(text)
