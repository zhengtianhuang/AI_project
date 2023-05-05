# templates.py
'''
引用庫
'''
from json import load
from pathlib import Path
import requests
import json
import os
'''
變數區
'''
bubblePath = Path(__file__).resolve().parent/'static/json/bubbles'
'''
class定義
'''


class Templates():
    '''
    新增一個flex_message
    '''

    def __init__(self):
        self.template = {
            "type": "carousel",
            "contents": []
        }
        self.t_count = 0

    def add_restaurant_bubble(self, image, name, rating, add, is_open):
        '''
        將寵物餐廳資訊加入氣泡中並顯示在Flex Message中
        :param image : 圖片的網址
        :param name : 名稱
        :param rating : 評分
        :param add: 
        :param is_open : 是否營業中
        '''
        bubble = load(
            open(f'{bubblePath}/restaurantBubble.json', 'r', encoding='utf-8'))
        # print(bubble)
        bubble["hero"]["url"] = str(image)
        bubble["body"]["contents"][0]["text"] = str(name)
        bubble["body"]["contents"][1]["contents"][5]["text"] = str(rating)
        bubble["body"]["contents"][3]["contents"][1]["text"] = str(add)
        bubble["body"]["contents"][4]["contents"][1]["text"] = str(is_open)

        # 替換的星星圖片
        HalfStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_half_14.png'
        EmptyStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_empty_14.png'

        # 判斷評論的整數部分有多少灰色星星
        empty_star = int((5 - rating) // 1)
        for i in range(empty_star):
            bubble["body"]["contents"][1]["contents"][4-i]["url"] = EmptyStar

        # 判斷評論的小數部分轉換的星星樣子，小數點落在3-7之間為半顆星
        dot_star = round(rating % 1 * 10)
        if dot_star < 8 and dot_star > 2:
            bubble["body"]["contents"][1]["contents"][4-empty_star]["url"] = HalfStar
        elif dot_star <= 2:
            bubble["body"]["contents"][1]["contents"][4-empty_star]["url"] = EmptyStar

        # 抓取google knowledge graph中的商家資訊
        params = {
                    "api_key": '7bec1da4ca2d934e97d542f96113cad7e2b7052e13098b7741416c75e8221073',
                    "engine": "google",
                    "q": name,
                    "google_domain": "google.com.tw",
                    "hl": "zh-tw",
                    "gl": "tw",
                    "tbs": "restaurant"
                }
        request_url = "https://serpapi.com/search.json?engine=google&q=" + name
        response = requests.get(request_url, data=params)
        response.encoding = 'uft-8'
        content = response.json()
        if "knowledge_graph" not in content:
            pass
        else:
            try:
                if "website" in content["knowledge_graph"]:
                    website = content["knowledge_graph"]["website"]
                    bubble["hero"]["action"]["uri"] = website
                if "菜單_links" in content["knowledge_graph"]:
                    menu_link = content["knowledge_graph"]["菜單_links"][0]["link"]
                    bubble["footer"]["contents"][0]["action"]["uri"] = menu_link
                if "merchant_description" in content["knowledge_graph"]:
                    merchant_desc = content["knowledge_graph"]["merchant_description"]
                    bubble["footer"]["contents"][1]["action"]["data"] = f"action={merchant_desc}&message_id=get_m_d"
            except (KeyError, IndexError):
                pass

        self.template["contents"].append(bubble)

    def add_pet_bubble(self, image, name, breed, emo, time):
        '''
        將寵物資訊加入氣泡中並顯示在Flex Message中
        :param image : 寵物圖片的網址
        :param name : 寵物名稱
        :param breed: 寵物品種
        :param emo: 寵物情緒
        :param time: 距離上次寵物分析間隔多久時間
        '''
        # 載入寵物資料bubble設定
        bubble = load(open(f'{bubblePath}/pet.json', 'r', encoding='utf-8'))

        # 設定寵物資訊
        bubble["hero"]["url"] = str(image)
        bubble["body"]["contents"][0]["text"] = str(name)
        bubble["body"]["contents"][1]["contents"][0]["contents"][2]["text"] = str(
            breed)
        bubble["body"]["contents"][1]["contents"][1]["contents"][2]["text"] = str(
            emo)
        bubble["body"]["contents"][2]["text"] = str(time)

        # 設定Footer的action data, 開頭數字為此人第幾隻寵物
        bubble["footer"]["contents"][0]["action"]["data"] = f"{self.t_count}更改照片"
        bubble["footer"]["contents"][1]["action"]["data"] = f"{self.t_count}更改名字"
        bubble["footer"]["contents"][2]["action"]["data"] = f"{self.t_count}更改品種"
        bubble["footer"]["contents"][3]["action"]["data"] = f"{self.t_count}刪除"
        bubble["footer"]["contents"][3]["action"]["text"] = "寵物資料"

        # 將bubble加入template的contents
        self.template["contents"].append(bubble)
        self.t_count += 1  # 用於判斷用戶按第幾個按鈕來確認要對第幾隻寵物資料更動
