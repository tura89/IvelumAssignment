from flask import Flask, request
from bs4 import BeautifulSoup
import requests

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8080

TARGET_HOST = 'https://news.ycombinator.com'

app = Flask(__name__)


def modify_response_content(response):
    """Modify response so that every word of length 6 is followed by ™."""
    soup = BeautifulSoup(response.content, 'html.parser')

    for text in soup.find_all(text=True):
        words = text.string.split(' ')
        for i, word in enumerate(words):
            # TODO: account for commas and other signs
            if len(word) == 6:
                words[i] = f'{word}™'
        content = ' '.join(words)

        # replace original text with modified one
        text.replace_with(BeautifulSoup(content, 'html.parser'))

    # return encoded content
    return soup.encode()


@app.route('/', defaults={'s': ''})
@app.route('/<string:s>')
def home(s):
    suffix = request.url.split(str(LOCAL_PORT))[1]
    response = requests.get(TARGET_HOST + suffix)

    modified_content = modify_response_content(response)

    return modified_content, response.status_code


if __name__ == '__main__':
    app.run(
        debug=True,
        host=LOCAL_HOST,
        port=LOCAL_PORT
    )
