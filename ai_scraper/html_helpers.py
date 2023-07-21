import logging

from bs4 import BeautifulSoup
import htmlmin


logger = logging.getLogger(__name__)


# list of tags to filter
FILTER_TAGS = ["script", "style", "header", "footer", "img", "nav", "aside",
"iframe", "audio", "video",, "svg", "canvas",
"blockquote", "figure", "time", "progress","wow-image","option", "script"]
FILTER_ATTRS = ["style", "href", "src"]

def preprocess_html(html: str) -> str:
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
    time.sleep(2)
    html_ = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html_, 'html.parser')
    for script in soup(['script', 'style', 'header', 'footer', 'nav', 'aside',
                                            'iframe', 'audio', 'video', 'svg', 'canvas',
                                            'blockquote', 'figure', 'time', 'progress','option','input','img']):
        script.extract()
    main_content = soup.find('div', {'class': 'main-content'})

    if not main_content:
        main_content = soup.body  # If no specific tags are found, use the entire body

    for tag in main_content.find_all():
        for attribute in ["name", "style"]:
            del tag[attribute]

    cleaned_html = str(main_content)

    minified_html = htmlmin.minify(cleaned_html, remove_empty_space=True)
    soup = BeautifulSoup(minified_html, 'html.parser')
    print(soup.prettify())