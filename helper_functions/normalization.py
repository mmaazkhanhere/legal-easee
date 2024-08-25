import markdown
from bs4 import BeautifulSoup

import re

def normalize_text(text):
    """
    Converts markdown text to plain text and normalizes it by removing special characters,
    excessive spaces, and standardizing the format for case-insensitive comparison.

    Parameters:
        text (str): The markdown text to be normalized.

    Returns:
        str: The normalized plain text.

    """
    # Convert markdown to plain text
    html_content = markdown.markdown(text)

    # Parse the HTML to extract plain text
    soup = BeautifulSoup(html_content, "html.parser")
    plain_text = soup.get_text()

    plain_text = re.sub(r'\s+', ' ', plain_text)  # Replace multiple spaces with a single space

    plain_text = plain_text.strip()  # Remove any leading or trailing whitespace

    plain_text = plain_text.lower()  # COnvert the entire text to lowercase to ensure case-insensitive comparison

    # replace sequences of underscore with a placeholder
    plain_text = re.sub(r'_+', '[underscore]', plain_text)

    return plain_text