from json import load
from linebot.models import (FlexSendMessage)


def template(a, b):
    # 給兩個長度為5的list參數(a景點名稱和b圖片連結)，設計呈現方式
    FlexMessage = load(
        open('./json/card.json', 'r', encoding='utf-8'))
    return FlexSendMessage("flex", FlexMessage)


def spider(a, b):
    # 這裡給經緯度要回傳兩個長度為5的list參數(景點名稱和圖片連結)
    return "兩個list"
