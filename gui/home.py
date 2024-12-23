from flask import Flask, render_template
from js_api import BrotheroJSApi
import webview

server = Flask(__name__)


@server.route("/")
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    window = webview.create_window('Brothero', server, js_api=BrotheroJSApi())
    webview.start(None, window)
