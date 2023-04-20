import requests
from database import append_pet, user_id_exists
import time
from pathlib import Path
import os
staticPath = Path(__file__).resolve().parent/'static'


def spider(latitude, longitude):
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
            return 4
        return self.steps[user_id]

    def _save_img(self, id, content):
        timestamp = str(int(time.time()))
        # 将文件保存到本地文件系统
        filename = f"{id}-{timestamp}.jpg"
        photo_path = os.path.join(staticPath, 'img', filename)
        with open(photo_path, 'wb') as f:
            for chunk in content.iter_content():
                f.write(chunk)
        return filename

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
            return "你傳的不是圖片！"
        else:
            return (f"發生錯誤step:{step}")

    def save_pet_img(self, user_id, img_id, content):
        self.steps[user_id] = 0
        file_name = self._save_img(img_id, content)
        print(f"{user_id},{self.name[user_id]},{self.breed[user_id]}")
        user_id_exists(user_id)
        append_pet(user_id, self.name[user_id],
                   file_name, self.breed[user_id])
        return (f"名字：{self.name[user_id]},品種：{self.breed[user_id]}")
