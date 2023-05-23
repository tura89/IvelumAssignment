from flask import Flask

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8080

TARGET_HOST = 'https://news.ycombinator.com'

app = Flask(__name__)


if __name__ == '__main__':
    app.run(
        debug=True,
        host=LOCAL_HOST,
        port=LOCAL_PORT
    )
