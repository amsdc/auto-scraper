import logging

from bs4 import BeautifulSoup
import htmlmin
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from lxml import html
import requests
import htmlmin
from pprint import pprint
import openai
import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import selenium
from typing import Optional
import time
import traceback
import os


logger = logging.getLogger(__name__)


# list of tags to filter
FILTER_TAGS = ["script", "style", "header", "footer", "img", "nav", "aside",
"iframe", "audio", "video", "svg", "canvas",
"blockquote", "figure", "time", "progress","wow-image","option", "script"]
FILTER_ATTRS = ["style", "href", "src"]

def preprocess_html(url: str) -> str:
    """preprocess_html 
    
    Clean up non-content parts of an HTML page

    Args:
        html (str): The HTML content to be cleaned

    Returns:
        str: The cleaned HTML
    """
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    option.add_argument('user-agent={0}'.format(user_agent))
    browser = webdriver.Chrome(executable_path='/Users/dhruvroongta/Downloads/chromedriver_mac_arm64/chromedriver', options=option)
    browser.get(url)
    time.sleep(3)
    html_ = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html_, 'html.parser')
    for script in soup(['script', 'style', 'header', 'footer', 'nav', 'aside',
                                            'iframe', 'audio', 'video', 'svg', 'canvas',
                                            'blockquote', 'figure', 'time', 'progress','option','input','img']):
        script.extract()
    

    # main_content = soup.find('div', {'class': 'main-content'})
    # print(main_content)
    main_content = soup.body
    # if not main_content:
    #     main_content = soup.body  # If no specific tags are found, use the entire body

    for tag in main_content.find_all():
        for attribute in ["name", "style"]:
            del tag[attribute]

    cleaned_html = str(main_content)

    minified_html = htmlmin.minify(cleaned_html, remove_empty_space=True)
    soup = BeautifulSoup(minified_html, 'html.parser')
    return soup.prettify()
    #print(soup.prettify())