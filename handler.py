# handler.py
'''
引用庫
'''
from utils import (return_pet_restaurants, PetCreator, is_dog)
from templates import Templates
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction,
                            TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
from dotenv import load_dotenv
import os
from database import db_delete_pet, db_search_pet
from pathlib import Path
import re
from Tasks.train_model.predict import predict_emotion
'''
變數區
'''
# 載入 .env 文件中的環境變數
load_dotenv(str(Path(__file__).resolve().parent/"Secret/secret.env"))
# 使用 os 模組獲取環境變數的值
handler = WebhookHandler(os.getenv('CHANNEL_ACCESS_TOKEN'))
line_bot_api = LineBotApi(os.getenv('CHANNEL_SECRET'))
img_path = Path(__file__).resolve().parent/'static/img'
pet = PetCreator()
'''
函式區
'''


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    '''
    處理文字訊息
    '''
    message = event.message.text
    user_id = event.source.user_id
    return_text = "需要幫忙嗎～"  # 預設回傳文字
    if_update = pet.update_pet(user_id, message)  # 確認是否在更新寵物資料流程
    if_create = pet.create_pet(user_id, message)  # 確認是否在新增寵物資料流程

    if if_update:
        return_text = if_update
        message = "寵物資料"  # 繼續執行寵物資料
    elif if_create:
        return_text = if_create
    elif message == "新增資料":
        pet.start_create_pet(user_id)
        return_text = "請輸入寵物名字"
    if message == "寵物資料":
        petTemplate = Templates()
        result = db_search_pet(user_id)
        if len(result) > 0:
            for row in result:
                imgUrl = os.path.join(
                    os.getenv('WEBHOOK_URL'), 'static/img', row[1])
                petTemplate.add_pet_bubble(imgUrl, row[0], row[2], "無", "未新增")
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage("flex", petTemplate.template)
            )
        return_text = "查無資料"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=return_text
                        )
    )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    '''
    處理位置訊息
    '''
    restaurants = return_pet_restaurants(
        event.message.latitude, event.message.longitude)
    rtTemplate = Templates()
    if len(restaurants) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="查無資料")
        )
        return
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
    '''
    處理圖片訊息
    '''
    return_text = "這不是狗狗~"  # 預設回傳
    user_id = event.source.user_id
    if isinstance(event.message, ImageMessage):
        img_id = event.message.id
        content = line_bot_api.get_message_content(img_id)
        if_update_pet = pet.update_pet(
            user_id=user_id, img_id=img_id, content=content)
        if_create_pet = pet.create_pet(
            user_id=user_id, img_id=img_id, content=content)
        if if_update_pet:
            return_text = if_update_pet
        elif if_create_pet:
            return_text = if_create_pet
        else:  # 情緒分析
            content = line_bot_api.get_message_content(img_id)
            img_name = pet._save_img(user_id, content)
            pet_name_tp_action = []
            if is_dog(img_path/img_name):
                emo_arg = predict_emotion(str(img_path/img_name))
                result = db_search_pet(user_id)
                if len(result) > 0:
                    for i, row in enumerate(result):
                        pet_name_tp_action.append(
                            PostbackTemplateAction(label=row[0], data=f"{user_id}新增{i}情緒{emo_arg}"))
                    pet_name_tp_action.append(
                        PostbackTemplateAction(label="其他", data=f"其他"))
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='選擇寵物名字',
                                text='請選擇',
                                actions=pet_name_tp_action
                            )
                        ))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(return_text)
    )


@handler.add(PostbackEvent)
def handle_message(event):
    '''
    處理postback訊息
    '''
    s = event.postback.data
    user_id = event.source.user_id
    updata_matchs = []  # 建立符合的pattern
    updata_matchs.append(re.search(r'^(\d+).*(更改照片)$', s))
    updata_matchs.append(re.search(r'^(\d+).*(更改名字)$', s))
    updata_matchs.append(re.search(r'^(\d+).*(更改品種)$', s))
    for i, match in enumerate(updata_matchs):
        if match:
            num = int(match.group(1))  # 抓字串開頭的寵物編號
            pet.start_update_pete(user_id, i+1, num)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(match.group(2))
            )

    delete_match = re.search(r'^(\d+).*(刪除)$', s)
    if delete_match:
        num = int(delete_match.group(1))
        db_delete_pet(user_id, num)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("成功刪除")
        )

    emo_match = re.match(r'(\w+)新增(\d+)情緒(\d+)', s)
    if emo_match:
        user_id = emo_match.group(1)
        pet_num = emo_match.group(2)
        emo_arg = emo_match.group(3)
        emo_list = ["生氣", "開心", "放鬆", "難過"]
        # print(user_id, i, emo_arg)
        pet_result = db_search_pet(user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                f"{pet_result[int(pet_num)][0]}現在很{emo_list[int(emo_arg)]}")
        )
