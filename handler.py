from utils import (spider, PetCreator, save_img)
from templates import templates
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (
    TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage)
pet = PetCreator()
handler = WebhookHandler('adef5f3ce019ca875e5fe10c1dff3b15')
line_bot_api = LineBotApi(
    '80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU=')


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
        TextSendMessage(text=message)
    )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    restaurants = spider(event.message.latitude, event.message.longitude)
    # print(restaurants)
    rtTemplate = templates()
    for i, d in enumerate(restaurants):
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


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    # 获取图片消息内容
    message = event.message
    if isinstance(message, ImageMessage):
        # 获取图片 ID 和文件名
        image_id = message.id
        # 使用 LineBot SDK 下载图片
        content = line_bot_api.get_message_content(image_id)
        print(content)
        save_img(image_id, content)
