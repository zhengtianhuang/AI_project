import json
import requests
from json import load


class templates():
    def __init__(self):
        self.template = {
            "type": "carousel",
            "contents": []
        }

    def add_restaurant_bubble(self, name, location):
        bubble = load(
            open('./json/bubbles/restaurantBubble.json', 'r', encoding='utf-8'))
        bubble["body"]["contents"][0]["text"] = name
        bubble["body"]["contents"][3]["contents"][1]["text"] = location
        self.template["contents"].append(bubble)


def spider(latitude, longitude):
    # 設置地圖API的URL和參數
    api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude}, {longitude}",  # 經緯度，這裡是台北市中正區的座標
        "radius": "500",  # 搜尋半徑，單位是公尺
        "type": "restaurant",  # 搜尋類型，這裡是餐廳
        "key": "AIzaSyDZzAdeBHRqkDsNHUbO2fLTZnSey2hzkq8"  # 請填入自己的API Key
    }

    # 使用Requests發送HTTP請求
    response = requests.get(api_url, params=params)

    # 解析回應內容
    jsonParse = json.loads(response.text)
    results = jsonParse["results"]

    for result in results:
        name = result['name']
        rating = result['rating']
        vicinity = result['vicinity']
        print(f"名字：{name}\n 評分：({rating})\n 地址：{vicinity}")
    return results
