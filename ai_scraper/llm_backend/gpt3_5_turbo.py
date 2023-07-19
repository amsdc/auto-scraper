class OpenAILLM():
    """OpenAILLM 
    
    Class to interact with the gpt3.5 turbo api.
    
    Args:
        api_key (str): ChatGPT API key
    """
    def __init__(self, api_key):
        self,api_key = api_key
    
    def set_page(self, page):
        self.url = page
    
    def fetch_clean_html(self):
        pass
    
    def call_openai(self):
        pass