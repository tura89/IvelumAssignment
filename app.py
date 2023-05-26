"""Main app file."""
import re

import bs4
import requests
from bs4 import BeautifulSoup
from flask import Flask, request

from config import HN_LINKS, LOCAL_HOST, LOCAL_PORT, TARGET_HOST

app = Flask(__name__)


def modify_response_content(content):
    """
    Modify site content as per requirements.

    Each word of length 6 is appended by trademark symbol.
    All the links leading to hackernews lead to local website instead.

    :param content: contents of response from hacker news
    :return: modified content
    """
    soup = BeautifulSoup(content, 'html5lib')

    # word that contains exactly 6 alphabetic characters,
    # optionally followed by a punctuation mark
    pattern = r'(^| )([A-Za-z]){6}(?=[\s!.,?;:-]|$)'

    for node in soup.find_all(lambda tag: any(isinstance(t, bs4.NavigableString) for t in tag)):
        subnodes = [t for t in node.contents if isinstance(t, bs4.NavigableString)]
        for text in subnodes:
            if text.parent.name not in ['script', 'style']:
                res = re.sub(pattern, r'\g<0>™', str(text))
                text.replace_with(res)

    for link in soup.find_all('a', href=True):
        for hnl in HN_LINKS:
            link['href'] = link['href'].replace(hnl, '/')

    return soup.encode()


@app.route('/', defaults={'path': ''})
@app.route('/<string:path>')
def home(path):  # pylint: disable=unused-argument
    """Proxy server for Hacker News."""
    url_parts = request.url.split(str(request.url_root))
    suffix = '' if len(url_parts) <= 1 else url_parts[1]  # get url path

    response = requests.get(TARGET_HOST + suffix, timeout=15)

    content = response.content.decode('utf-8')
    modified_content = modify_response_content(content)

    return modified_content, response.status_code


if __name__ == '__main__':
    app.run(
        debug=True,
        host=LOCAL_HOST,
        port=LOCAL_PORT
    )
