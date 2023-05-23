import re

from config import LOCAL_HOST, LOCAL_PORT, TARGET_HOST

from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def modify_response_content(response):
    """Modify response so that every word of length 6 is followed by ™."""
    soup = BeautifulSoup(response.content, 'html.parser')

    for text in soup.find_all(text=True):
        words = text.string.split(' ')
        for i, word in enumerate(words):
            # account for commas and other signs
            word_text = re.sub(r'[\W_]', '', word)

            if len(word_text) == 6:
                words[i] = word.replace(word_text, f'{word_text}™')

        content = ' '.join(words)

        # replace original text with modified one
        text.replace_with(BeautifulSoup(content, 'html.parser'))

    # return encoded content
    return soup.encode()


@app.route('/', defaults={'s': ''})
@app.route('/<string:s>')
def home(s):
    url_parts = request.url.split(str(request.url_root))
    suffix = '' if len(url_parts) <= 1 else url_parts[1]  # get url path

    response = requests.get(TARGET_HOST + suffix)

    modified_content = modify_response_content(response)

    return modified_content, response.status_code


if __name__ == '__main__':
    app.run(
        debug=True,
        host=LOCAL_HOST,
        port=LOCAL_PORT
    )
