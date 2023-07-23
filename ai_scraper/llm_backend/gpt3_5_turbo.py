import logging
import requests
import logging
from abc import ABC, abstractmethod
import requests
import html_helpers
import time
from typing import Optional
import openai
from prompts import sys_prompt_scrapper,sys_prompt_sqlite,field_prompt
import json


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
    
'''    @abstractmethod
    def generate_scraper(self):
        pass
'''

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
        return html_string

    def extract_data(self,html_string,k:Optional[int] = 30000):
        total_data = []
        for i in range(0,len(html_string),k):
            #ADD TOO LONG INPUT THING
            input_template = {
                "spec_version": "1.0",
                "page_url": self.url,
                "page_html": str(html_string)[i:i+k],
                "metadata": {
                    "type": "tabular",
                    "attributes": self.fields
                }
            }
            
            completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo-16k",
                temperature = 0.0,
                messages =  [{"role": "system", "content": sys_prompt_scrapper}, {"role": "user", "content": str(input_template)}]
            )
            
            text = completion['choices'][0]['message']['content']
            text = """{}""".format(text).replace("\\"," ").rstrip("`")
            text = json.loads(text)
            data = text["content"]
            total_data.extend(data)
        
        return(total_data)

    def suggest_fields(self,k:Optional[int] = 30000):
        input_template = {
            "spec_version": "1.0",
            "page_url": self.url,
            "page_html": str(self.html_string)[0:k],
        }
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            temperature = 0.0,
            messages =  [{"role": "system", "content": field_prompt}, {"role": "user", "content": str(input_template)}]
        )
            
        print(completion)
        text = completion['choices'][0]['message']['content']
        self.fields = text
        print(text)
        return(text)
    
    def auto_filter(self,table_title,query,json_array,):

        input_template = {
            "Title":table_title,
            "Columns and Types":self.fields,
            "Sample Data": json_array[:3],
            "Query": query
        }

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.0,
            messages =  [{"role": "system", "content": sys_prompt_sqlite}, {"role": "user", "content": str(input_template)}]
        )
            
        print(completion)
        text = completion['choices'][0]['message']['content']
        print(text)
        return text

scraper = OpenAIScraper("https://devpost.com/hackathons")
html = scraper.get_html()
print(html)
fields = scraper.suggest_fields()
time.sleep(5)
json_data = scraper.extract_data(html)
print(json_data)