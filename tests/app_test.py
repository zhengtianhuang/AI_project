# app.py
# =============庫==================
from flask import Flask, request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
# =============副程式==================
from handler import handler
# =============變數==================
app = Flask(__name__)
# ==========main============


@app.route("/", methods=['GET'])
def test():
    return "ok"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


if __name__ == "__main__":
    app.run(port=8080)
