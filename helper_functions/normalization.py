import markdown
from bs4 import BeautifulSoup

import re

def normalize_text(text):
    # Convert markdown to plain text
    html_content = markdown.markdown(text)
    soup = BeautifulSoup(html_content, "html.parser")
    plain_text = soup.get_text()

    # Normalize: remove special characters, excessive spaces, etc.
    plain_text = re.sub(r'\s+', ' ', plain_text)  # Replace multiple spaces with a single space
    plain_text = plain_text.strip()  # Trim leading and trailing whitespace
    plain_text = plain_text.lower()  # Convert to lowercase for case-insensitive comparison

    # Replace multiple underscores with a single placeholder (e.g., "___" becomes "[underscore]")
    plain_text = re.sub(r'_+', '[underscore]', plain_text)

    return plain_text