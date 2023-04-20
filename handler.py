from utils import (spider, PetCreator)
from templates import templates
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (
    TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
from dotenv import load_dotenv
import os
from database import search_pet
from pathlib import Path
import re
# 載入 .env 文件中的環境變數
load_dotenv("secret.env")
# 使用 os 模組獲取環境變數的值
handler = WebhookHandler(os.getenv('CHANNEL_ACCESS_TOKEN'))
line_bot_api = LineBotApi(os.getenv('CHANNEL_SECRET'))
pet = PetCreator()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    text = "需要幫忙嗎～"
    user_id = event.source.user_id
    ifUpdate = pet.update_pet(user_id, message)
    print(ifUpdate)
    creatPetStep = pet.check_create_pet(user_id)
    if ifUpdate:
        text = ifUpdate
    elif creatPetStep:
        text = pet.create_pet(user_id, creatPetStep, message)
    elif message == "新增資料":
        pet.start_create_pet(user_id)
        text = "請輸入寵物名字"
    elif message == "寵物資料":
        petTemplate = templates()
        result = search_pet(user_id)
        for row in result:
            imgUrl = os.path.join(
                os.getenv('WEBHOOK_URL'), 'static/img', row[1])
            petTemplate.add_pet_bubble(imgUrl, row[0], row[2], "無", "未新增")
            print(imgUrl)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage("flex", petTemplate.template)
        )
        return
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
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
    message = "cool~"
    user_id = event.source.user_id
    if isinstance(event.message, ImageMessage):
        creatPetStep = pet.check_create_pet(user_id)
        if creatPetStep == 4:
            # 获取图片 ID 和文件名
            image_id = event.message.id
            # 使用 LineBot SDK 下载图片
            content = line_bot_api.get_message_content(image_id)
            print(content)
            message = pet.save_pet_img(user_id, image_id, content)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(message)
    )


@handler.add(PostbackEvent)
def handle_message(event):
    s = event.postback.data
    user_id = event.source.user_id
    matchs = []
    matchs.append(re.search(r'^(\d+).*(更改照片)$', s))
    matchs.append(re.search(r'^(\d+).*(更改名字)$', s))
    matchs.append(re.search(r'^(\d+).*(更改品種)$', s))
    matchs.append(re.search(r'^(\d+).*(刪除)$', s))
    for i, match in enumerate(matchs):
        if match:
            num = int(match.group(1))
            print(num)  # 輸出 1
            pet.start_update_pete(user_id, i+1, num)
            print(i+1)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(match.group(2))
            )
    print(s)
