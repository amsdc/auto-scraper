from bs4 import BeautifulSoup
import minify_html

# list of tags to filter
FILTER_TAGS = ["script", "style", "header", "footer", "img", "nav", "aside",
"iframe", "audio", "video", "form", "svg", "canvas",
"blockquote", "figure", "time", "progress","wow-image","option", "script"]
FILTER_ATTRS = ["id", "name", "class", "style"]

def preprocess_html(html: str) -> str:
    """preprocess_html 
    
    Clean up non-content parts of an HTML page

    Args:
        html (str): The HTML content to be cleaned

    Returns:
        str: The cleaned HTML
    """
    soup = BeautifulSoup(html, "lxml")
    for script in soup(FILTER_TAGS):
        script.extract()

    main_content = soup.find("div", class_="main-content")
    if main_content is None:
        main_content = soup.body  # If no specific tags are found, use the entire body

    for tag in main_content.find_all():
        for attribute in FILTER_ATTRS:
            del tag[attribute]
    
    for tag in soup.find_all():
        if not tag.contents:
            tag.extract()

    cleaned_html = str(main_content)
    print(".", cleaned_html)
    return minify_html.minify(cleaned_html, minify_js=True)