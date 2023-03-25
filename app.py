# app.py
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    '80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('adef5f3ce019ca875e5fe10c1dff3b15')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
