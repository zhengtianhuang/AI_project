import json
import requests
from json import load


class templates():
    def __init__(self):
        self.template = {
            "type": "carousel",
            "contents": []
        }

    def add_restaurant_bubble(self, image, name, rating, add, open):
        bubble = load(open('./json/bubbles/res.json', 'r', encoding='utf-8'))
        bubble["hero"]["action"]["uri"] = image
        bubble["body"]["contents"][0]["text"] = name
        bubble["body"]["contents"][1]["contents"][5]["text"] = rating
        bubble["body"]["contents"][3]["contents"][1]["text"] = add
        bubble["hero"]["contents"][4]["contents"][1]["text"] = open
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

def spider2(latitude, longitude):
    resInfoAll = list()
    GOOGLE_PLACES_API_KEY ="AIzaSyBt5lGoOVCzoKV9F03ZU9QwwI6rSxnI38Q"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    api_key = "AIzaSyBt5lGoOVCzoKV9F03ZU9QwwI6rSxnI38Q"
    types = "pet_store,veterinary_care"
    keyword = "寵物餐廳"
    radius = str(500)
    resPhotoPrfx = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400"
    query_url = f"{url}location={latitude},{longitude}&radius={radius}&types={types}&keyword={keyword}&key={api_key}&language=zh-TW"
    response = requests.get(query_url)
    res = response.json()
    
    if res["status"] == "OK":
        results = res["results"]
        for result in results:
            resInfo = dict()
            resInfo['resPhoto'] = f"{resPhotoPrfx}&photo_reference={(result['photos'][0])['photo_reference']}&key={api_key}"
            resInfo['resName'] = result["name"]
            resInfo['resRating'] = result["rating"]
            resInfo['resAdd'] = f"{result['plus_code']['compound_code'][-3:]}{result['vicinity']}"
            resInfo['resOpen'] = ""
            if result["opening_hours"]["open_now"] == True:
                resInfo['resOpen'] = "營業中"
                resInfoAll.append(resInfo)
            else:
                resInfo['resOpen'] = "目前無營業"
                resInfoAll.append(resInfo)
    else:
        print("Request failed.")
    print(resInfoAll)  
    return resInfoAll
