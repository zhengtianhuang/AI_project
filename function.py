import json
import requests
from json import load
from server import append_pet, user_id_exists


class templates():
    def __init__(self):
        self.template = {
            "type": "carousel",
            "contents": []
        }

    def add_restaurant_bubble(self, image, name, rating, add, isOpen):
        print("==="*20)
        bubble = load(
            open('./json/bubbles/restaurantBubble.json', 'r', encoding='utf-8'))
        # print(bubble)
        bubble["hero"]["url"] = str(image)
        bubble["body"]["contents"][0]["text"] = str(name)
        bubble["body"]["contents"][1]["contents"][5]["text"] = str(rating)
        bubble["body"]["contents"][3]["contents"][1]["text"] = str(add)
        bubble["body"]["contents"][4]["contents"][1]["text"] = str(isOpen)
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
    GOOGLE_PLACES_API_KEY = "AIzaSyBt5lGoOVCzoKV9F03ZU9QwwI6rSxnI38Q"
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
    # print(resInfoAll)
    return resInfoAll


# step = {}


# def startCreatePet(userId):
#     global step
#     step[userId] = 1


# def checkCreatePet(userId):
#     global step
#     if userId not in step:
#         return 0
#     elif step[userId] == 1:
#         step[userId] = 2
#     elif step[userId] == 2:
#         step[userId] = 3
#     elif step[userId] == 3:
#         step[userId] = 0
#         return 4
#     return step[userId]


# def creatPet(step, data):
#     if step == 2:
#         return f"你的寵物名字是{data},請輸入品種"
#     elif step == 3:
#         return f"品種為{data},請傳一張照片！"
#     elif step == 4:
#         return "真可愛！"
#     else:
#         return (f"發生錯誤step:{step}")

class PetCreator:
    def __init__(self):
        self.steps = {}
        self.breed = {}
        self.name = {}

    def start_create_pet(self, user_id):
        self.steps[user_id] = 1

    def check_create_pet(self, user_id):
        if user_id not in self.steps:
            return 0
        elif self.steps[user_id] == 1:
            self.steps[user_id] = 2
        elif self.steps[user_id] == 2:
            self.steps[user_id] = 3
        elif self.steps[user_id] == 3:
            self.steps[user_id] = 0
            return 4
        return self.steps[user_id]

    def create_pet(self, user_id, step, data):
        if step == 2:
            self.name[user_id] = data
            return f"你的寵物名字是{data},請輸入品種"
        elif step == 3:
            self.breed[user_id] = data
            return f"品種為{data},請傳一張照片！"
        elif step == 4:
            # user_id_exists(user_id)
            # append_pet(user_id, self.name[user_id],
            #            data, self.breed[user_id])
            print(
                f"{user_id},{self.name[user_id]},{data},{self.breed[user_id]}")
            return "真可愛！"
        else:
            return (f"發生錯誤step:{step}")
