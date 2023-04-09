from json import load
from linebot.models import (FlexSendMessage)


class templates():
    def __init__(self):
        self.template = {
            "type": "carousel",
            "contents": []
        }

    def add_restaurant_bubble(self, name, location):
        bubble = load(
            open('./json/bubbles/food.json', 'r', encoding='utf-8'))
        bubble["body"]["contents"][0]["text"] = name
        bubble["body"]["contents"][3]["contents"][1]["text"] = location
        self.template["contents"].append(bubble)


def template(a, b):
    # 給兩個長度為5的list參數(a景點名稱和b圖片連結)，設計呈現方式
    FlexMessage = load(
        open('./json/restaurant.json', 'r', encoding='utf-8'))
    return FlexSendMessage("flex", FlexMessage)


def spider(a, b):
    # 這裡給經緯度要回傳兩個長度為5的list參數(景點名稱和圖片連結)
    return "兩個list"
