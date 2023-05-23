"""Main app file."""
import re

import requests
from bs4 import BeautifulSoup
from flask import Flask, request

from config import LOCAL_HOST, LOCAL_PORT, TARGET_HOST

app = Flask(__name__)


def modify_response_content(response):
    """Modify response so that every word of length 6 is followed by ™."""
    soup = BeautifulSoup(response.content, 'html.parser')

    for text in soup.find_all(string=True):
        words = text.string.split(' ')
        for i, word in enumerate(words):
            # account for commas and other signs
            word_text = re.sub(r'[\W_]', '', word)

            if len(word_text) == 6:
                words[i] = word.replace(word_text, f'{word_text}™')

        content = ' '.join(words)

        # replace original text with modified one
        text.replace_with(BeautifulSoup(content, 'html.parser'))

    # make sure links to hacker news lead to local site
    hn_links = ['https://www.ycombinator.com', 'https://news.ycombinator.com']
    for link in soup.find_all('a', href=True):
        for hnl in hn_links:
            link['href'] = link['href'].replace(hnl, '/')

    # account for image sources
    for image in soup.find_all('img'):
        image['src'] = 'https://news.ycombinator.com/' + image['src']

    # return encoded content
    return soup.encode()


@app.route('/', defaults={'path': ''})
@app.route('/<string:path>')
def home(path):  # pylint: disable=unused-argument
    """Proxy server for Hacker News."""
    url_parts = request.url.split(str(request.url_root))
    suffix = '' if len(url_parts) <= 1 else url_parts[1]  # get url path

    response = requests.get(TARGET_HOST + suffix, timeout=15)

    modified_content = modify_response_content(response)

    return modified_content, response.status_code


if __name__ == '__main__':
    app.run(
        debug=True,
        host=LOCAL_HOST,
        port=LOCAL_PORT
    )
