# handler.py
'''
引用庫
'''
from utils import (return_pet_restaurants, PetCreator, is_dog, delta_time)
from line_templates import Templates
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (ButtonsTemplate, TemplateSendMessage, PostbackTemplateAction, ImageSendMessage,
                            TextSendMessage, FlexSendMessage, TextMessage, LocationMessage, MessageEvent, ImageMessage, PostbackEvent)
import os
from database import db_delete_pet, db_search_pet, db_append_emotion, db_search_emotion, db_get_emolist
from pathlib import Path
import re
from predict import predict_emotion
from dotenv import load_dotenv
'''
變數區
'''
# 使用 os 模組獲取環境變數的值
load_dotenv(str(Path(__file__).resolve().parent/"Secret/secret.env"))
handler = WebhookHandler(os.getenv('CHANNEL_ACCESS_TOKEN'))
line_bot_api = LineBotApi(os.getenv('CHANNEL_SECRET'))
static_path = Path(__file__).resolve().parent/'static'
pet_img_path = Path(__file__).resolve().parent/'static/pet_img'
pet = PetCreator()
emo_list = db_get_emolist()
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
                img_url = os.path.join(
                    os.getenv('WEBHOOK_URL'), 'static/pet_img', row[1])
                pet_id = row[3]
                emo_result = db_search_emotion(pet_id)
                if emo_result != None:
                    emo_index = int(emo_result[0])
                    updated_time = emo_result[1]
                    petTemplate.add_pet_bubble(
                        img_url, row[0], row[2], emo_list[emo_index], delta_time(updated_time))
                else:
                    petTemplate.add_pet_bubble(
                        img_url, row[0], row[2], "無", "未新增")
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage("flex", petTemplate.template)
            )
        return_text = "查無資料"
    elif message == "功能介紹":
        line_bot_api.reply_message(
            event.reply_token,
            [ImageSendMessage(preview_image_url=os.path.join(
                os.getenv('WEBHOOK_URL'), 'static', 'img', '5.png'), original_content_url=os.path.join(
                os.getenv('WEBHOOK_URL'), 'static', 'img', '5.png')), ImageSendMessage(preview_image_url=os.path.join(
                    os.getenv('WEBHOOK_URL'), 'static', 'img', '6.png'), original_content_url=os.path.join(os.getenv('WEBHOOK_URL'), 'static', 'img', '6.png'))])
    elif message == "寵物情緒分析":
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(preview_image_url=os.path.join(
                os.getenv('WEBHOOK_URL'), 'static', 'img', '6.png'), original_content_url=os.path.join(os.getenv('WEBHOOK_URL'), 'static', 'img', '6.png')
            )
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=return_text
                        )
    )


@ handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    '''
    處理位置訊息
    '''
    restaurants = return_pet_restaurants(
        event.message.latitude, event.message.longitude)
    rt_template = Templates()
    if len(restaurants) == 0:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="查無資料")
        )
        return
    for i, d in enumerate(restaurants):
        try:
            rt_template.add_restaurant_bubble(
                d['resPhoto'], d['resName'], d['resRating'], d["resAdd"], d["resOpen"])
        except Exception as e:
            print(e)
        if i > 8:
            break
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage("flex", rt_template.template)
    )


@ handler.add(MessageEvent, message=ImageMessage)
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
            img_name = pet._save_img(img_id, content)
            pet_name_tp_action = []
            if is_dog(pet_img_path/img_name):
                emo_arg = predict_emotion(str(pet_img_path/img_name))
                pet.delete_img(pet_img_path/img_name)  # 預測完後刪除照片
                result = db_search_pet(user_id)
                if len(result) > 0:
                    for i, row in enumerate(result):
                        pet_name_tp_action.append(
                            PostbackTemplateAction(label=row[0], data=f"{user_id}新增{row[3]}名字{row[0]}情緒{emo_arg}"))
                    pet_name_tp_action.append(PostbackTemplateAction(
                        label="其他", data=f"其他{emo_arg}"))
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
                    return
                else:  # 未新增任何寵物
                    return_text = f"您的寵物現在很{emo_list[emo_arg]}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(return_text)
    )


@ handler.add(PostbackEvent)
def handle_message(event):
    '''
    處理postback訊息
    '''
    s = event.postback.data
    user_id = event.source.user_id
    updata_matchs = []  # 建立符合的pattern
    emo_match = re.match(r'(\w+)新增(\d+)名字(\w+)情緒(\d+)', s)
    updata_matchs.append(re.search(r'^(\d+).*(請上傳新照片～)$', s))
    updata_matchs.append(re.search(r'^(\d+).*(請輸入新名字～)$', s))
    updata_matchs.append(re.search(r'^(\d+).*(請輸入新品種～)$', s))
    delete_match = re.search(r'^(\d+).*(刪除)$', s)
    other_pet_emo_match = re.match(r'其他(\d+)', s)
    for i, match in enumerate(updata_matchs):
        if match:
            num = int(match.group(1))  # 抓字串開頭的寵物編號(從0開始)
            pet.start_update_pete(user_id, i+1, num)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(match.group(2))
            )
    if delete_match:
        num = int(delete_match.group(1))
        img_name = db_search_pet(user_id)[num][1]
        pet.delete_img(pet_img_path/img_name)
        db_delete_pet(user_id, num)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("已刪除資料！")
        )
    elif emo_match:
        user_id = emo_match.group(1)
        pet_id = emo_match.group(2)
        pet_name = emo_match.group(3)
        emo_arg = emo_match.group(4)
        db_append_emotion(pet_id, emo_arg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                f"您的{pet_name}現在很{emo_list[int(emo_arg)]}!")
        )
    elif other_pet_emo_match:
        emo_arg = other_pet_emo_match.group(1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                f"您的寵物現在很{emo_list[int(emo_arg)]}!")
        )

    #
    match_m_d = re.search(r'message_id=get_m_d', s)
    if match_m_d:
        action = re.search(r'action=([^&]+)', s).group(1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(action)
        )
