import pickle
import unittest
import os

import ai_scraper.llm_backend.gpt3_5_turbo as LLMCaller

class TestLLMCaller(unittest.TestCase):
    def setUp(self):
        self.llm_caller = LLMCaller.OpenAIScraper(os.environ.get("OPENAPI_KEY"))
        
    def test_fetch_url(self):
        self.llm_caller.set_page("https://advaith.pythonanywhere.com/a"
                                 "msdc/software/listAll?sortBy=lastupd"
                                 "ated&order=desc")
        self.assertEqual(self.llm_caller.fetch_clean_html(),
                         pickle.load(open("testcontent/test_fetch_url", "rb")))


if __name__ == "__main__":
    unittest.main(verbosity=2)