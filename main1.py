import requests
from bs4 import BeautifulSoup
from lxml import html
import requests
import htmlmin

def preprocess_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(['script', 'style', 'header', 'footer', 'img', 'nav', 'aside',
                                           'iframe', 'audio', 'video', 'form', 'svg', 'canvas',
                                           'blockquote', 'figure', 'time', 'progress','wow-image','option']):
        script.extract()

    main_content = soup.find('div', {'class': 'main-content'})
    if not main_content:
        main_content = soup.find('article')
    if not main_content:
        main_content = soup.body  # If no specific tags are found, use the entire body

    for tag in main_content.find_all():
        for attribute in ["id", "name", "style"]:
            del tag[attribute]
    
    for tag in soup.find_all():
        if not tag.contents:
            tag.extract()

    cleaned_html = str(main_content)
    minified_html = htmlmin.minify(cleaned_html, remove_empty_space=True)
    soup = BeautifulSoup(minified_html, 'html.parser')
    return soup.prettify()

class OpenAICaller:
    def __init__(self,api_key,url):
        self,api_key = api_key
        self.url = url
    
    def get_html(self):
        return preprocess_html(requests.get(url).text)
        
    def call_openai(self):
        pass

html_string = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>EXAMPLE COMPANY - BOARD OF DIRECTORS</title>
    </head>
    <body>
        <div>
            <h1>Example Company</h1>
            <h2>Board of DIRECTORS</h2>
        </div>

        <div>
            <div class="ng-bold"><a href="/directory/searchPerson.aspx?name=Angel%20Cabera&desg=President">Angel Cabera</a></div>
            <div class="table-row">President</div>
        </div>

        <div>
            <div class="ng-bold"><a href="/directory/searchPerson.aspx?name=Christie%20Stewart&desg=Dean">Christie Stewart</a></div>
            <div class="table-row">Dean</div>
        </div>
    </body>
</html>"""

print(preprocess_html(html_string))


