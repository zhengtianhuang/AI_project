# templates.py
'''
引用庫
'''
from json import load
import os
from pathlib import Path
from utils import return_pet_restaurant_details
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

    def add_restaurant_bubble(self, image, name, rating, address, is_open):
        '''
        將寵物餐廳資訊加入氣泡中並顯示在Flex Message中
        :param image : 圖片的網址
        :param name : 名稱
        :param rating : 評分
        :param address: 餐廳地址
        :param is_open : 是否營業中
        '''
        bubble = load(
            open(f'{bubblePath}/restaurant.json', 'r', encoding='utf-8'))
        # print(bubble)
        bubble["hero"]["url"] = str(image)
        bubble["body"]["contents"][0]["text"] = str(name)
        bubble["body"]["contents"][1]["contents"][5]["text"] = str(rating)
        bubble["body"]["contents"][3]["contents"][1]["text"] = str(address)
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
            bubble["body"]["contents"][1]["contents"][4 -
                                                      empty_star]["url"] = HalfStar
        elif dot_star <= 2:
            bubble["body"]["contents"][1]["contents"][4 -
                                                      empty_star]["url"] = EmptyStar
        content = return_pet_restaurant_details(name)
        try:
            if "website" in content["knowledge_graph"]:
                website = content["knowledge_graph"]["website"]
                bubble["hero"]["action"]["uri"] = website
            else:
                bubble["hero"]["action"]["uri"] = os.getenv("WEBHOOK_URL")
            if "菜單_links" in content["knowledge_graph"]:
                menu_link = content["knowledge_graph"]["菜單_links"][0]["link"]
                bubble["footer"]["contents"][0]["action"]["uri"] = menu_link
            else:
                bubble["footer"]["contents"][0]["action"]["uri"] = os.getenv(
                    "WEBHOOK_URL")
            if "merchant_description" in content["knowledge_graph"]:
                merchant_desc = content["knowledge_graph"]["merchant_description"]
                bubble["footer"]["contents"][1]["action"][
                    "data"] = merchant_desc[1:-1]
        except (KeyError, IndexError) as ex:
            print(ex)
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
        bubble["footer"]["contents"][0]["action"]["data"] = f"{self.t_count}請上傳新照片～"
        bubble["footer"]["contents"][1]["action"]["data"] = f"{self.t_count}請輸入新名字～"
        bubble["footer"]["contents"][2]["action"]["data"] = f"{self.t_count}請輸入新品種～"
        bubble["footer"]["contents"][3]["action"]["data"] = f"{self.t_count}刪除"
        bubble["footer"]["contents"][3]["action"]["text"] = "寵物資料"

        # 將bubble加入template的contents
        self.template["contents"].append(bubble)
        self.t_count += 1  # 用於判斷用戶按第幾個按鈕來確認要對第幾隻寵物資料更動
