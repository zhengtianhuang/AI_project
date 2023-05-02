# templates.py
'''
引用庫
'''
from json import load
from pathlib import Path
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

        # 將bubble加入template的contents
        self.template["contents"].append(bubble)
        self.t_count += 1  # 用於判斷用戶按第幾個按鈕來確認要對第幾隻寵物資料更動
