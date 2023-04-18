# app.py
# =============庫==================
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, FlexSendMessage, LocationSendMessage, LocationMessage
)
# =============副程式==================

from function import (templates, spider2, PetCreator)
from server import (user_id_exists)
# =============變數==================
app = Flask(__name__)

line_bot_api = LineBotApi(
    '80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('adef5f3ce019ca875e5fe10c1dff3b15')

pet = PetCreator()
# ==========這裡基本不用動============


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

# =============收到文字訊息==================


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    user_id = event.source.user_id
    creatPetStep = pet.check_create_pet(user_id)
    if creatPetStep:
        message = pet.create_pet(user_id, creatPetStep, message)
    if message == "新增資料":
        pet.start_create_pet(user_id)
        message = "請輸入寵物名字"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(message)
    )


# @handler.add(MessageEvent, message=TextMessage)
# def handle_text_message(event):
#     # get userId
#     user_id = event.source.user_id
#     print(user_id)
#     user_id_exists(user_id)
#     pet_name = '10'
#     pet_photo = 'ss.jpg'
#     pet_breed = '薩摩耶'
#     append_pet(user_id, pet_name, pet_photo, pet_breed)
# ========================================================若是位置訊息


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    restaurants = spider2(event.message.latitude, event.message.longitude)
    print(restaurants)
    rtTemplate = templates()
    for i, d in enumerate(restaurants):
        # print("+"*20)
        # print(d['resPhoto'])
        # print("+"*20)
        try:
            rtTemplate.add_restaurant_bubble(
                d['resPhoto'], d['resName'], d['resRating'], d["resAdd"], d["resOpen"])
        except Exception as e:
            print(e)
        if i > 8:
            break

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage("flex", rtTemplate.template)
    )


if __name__ == "__main__":
    app.run(port=8080)
