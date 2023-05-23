from flask import Flask, request
import requests

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8080

TARGET_HOST = 'https://news.ycombinator.com'

app = Flask(__name__)


@app.route('/', defaults={'s': ''})
@app.route('/<string:s>')
def home(s):
    suffix = request.url.split(str(LOCAL_PORT))[1]
    response = requests.get(TARGET_HOST + suffix)

    return response.content, response.status_code


if __name__ == '__main__':
    app.run(
        debug=True,
        host=LOCAL_HOST,
        port=LOCAL_PORT
    )
