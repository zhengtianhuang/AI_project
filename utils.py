# utils.py
'''
引用庫
'''
import requests
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from database import append_pet, user_id_exists, update_pet
import time
from pathlib import Path
import os
'''
變數區
'''
staticPath = Path(__file__).resolve().parent/'static'
'''
函式區
'''


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
    return resInfoAll


class PetCreator:
    '''
    用於新增寵物以及更改寵物資料的流程控制
    :ivar steps : 用於控制新增寵物流程
    :ivar update_col : 用於控制更改寵物資料哪個欄位
    :ivar updata_num : 判斷目前要做第幾隻寵物的資料更動
    :ivar name : 用戶回傳的寵物名字
    '''

    def __init__(self):
        self.steps = {}
        self.updateCol = {}
        self.updateNum = {}
        self.breed = {}
        self.name = {}

    def start_update_pete(self, user_id, col, num):
        '''
        開始更改寵物資料流程
        :param user_id : line用戶id
        :param col : 用於控制更改寵物資料哪個欄位
        :param num : 判斷目前要做第幾隻寵物的資料更動
        '''
        self.updateCol[user_id] = col
        self.updateNum[user_id] = num

    def start_create_pet(self, user_id):
        '''
        開始新增寵物流程
        '''
        self.steps[user_id] = 1

    def update_pet(self, user_id, data=0, img_id=0, content=0):
        '''
        更改寵物資料
        :param user_id : line用戶id
        :param data : 要更改的資料,通常就是抓用戶傳的文字訊息,若是圖片訊息,data請傳入 "他傳了圖片！"
        :return 0   : 沒有要更新資料
                其他 : 要回傳的文字訊息      
        '''
        col_name = "pet_name"
        if user_id not in self.updateCol or self.updateCol[user_id] == 0:
            return 0
        elif self.updateCol[user_id] == 1:  # 用戶按下更改圖片
            if self._update_pet_img(user_id, img_id, content):
                self.updateCol[user_id] = 0  # 更改完後回復初始階段
                return "成功更改"
            return "這不是圖片！"
        elif self.updateCol[user_id] == 2:  # 用戶按下更改名字
            col_name = "pet_name"
        elif self.updateCol[user_id] == 3:  # 用戶按下更改品種
            col_name = "pet_breed"
        update_pet(col_name, data, user_id, self.updateNum[user_id])
        self.updateCol[user_id] = 0  # 更改完後回復初始階段
        return f"成功更改{col_name}"

    def create_pet(self, user_id, data=0, img_id=0, content=0):
        '''
        新增一個寵物流程控制
        :param user_id : line用戶id
        :param data : 新增的資料內容,通常就是抓用戶傳的文字訊息
        :param img_id : line給的圖片id
        :param content : 圖片訊息內容
        :return 0   : 沒有在新增資料
                其他 : 要回傳的文字訊息 
        '''
        if user_id not in self.steps or self.steps[user_id] == 0:
            return 0
        elif self.steps[user_id] == 1:   # 第一階段輸入名字
            self.steps[user_id] += 1
            self.name[user_id] = data
            return f"你的寵物名字是{data},請傳一張照片"
        elif self.steps[user_id] == 2:   # 第二階段傳圖片
            if self._save_pet_img(user_id, img_id, content):
                self.steps[user_id] = 0  # 回復初始階段
                return (f"名字：{self.name[user_id]},品種：{self.breed[user_id]}")
            else:
                return "你傳的不是圖片！"
        else:
            return (f"發生錯誤step:{self.steps[user_id]}")

    def _save_img(self, img_id, content):
        '''
        將用戶傳的圖片保存到本地server
        :param img_id : line給的圖片id
        :param content : 圖片訊息內容
        :return    檔名 : 時間戳加img_id
        '''
        timestamp = str(int(time.time()))
        filename = f"{img_id}-{timestamp}.jpg"
        photo_path = os.path.join(staticPath, 'img', filename)
        with open(photo_path, 'wb') as f:
            for chunk in content.iter_content():
                f.write(chunk)
        return filename

    def _save_pet_img(self, user_id, img_id, content):
        '''
        將寵物圖片存入本地server,檔名存入db
        :param user_id : line用戶id
        :param img_id : line給的圖片id
        :return     1 : 成功 
                    0 : 失敗
        '''
        if img_id == 0:
            return 0
        file_name = self._save_img(img_id, content)
        img_url = os.path.join(
            os.getenv('WEBHOOK_URL'), 'static/img', file_name)
        self.breed[user_id] = return_image_breed(img_url)
        user_id_exists(user_id)
        append_pet(user_id, self.name[user_id],
                   file_name, self.breed[user_id])
        return 1

    def _update_pet_img(self, user_id, img_id, content):
        '''
        更新寵物圖像
        :param user_id : line用戶id
        :param img_id : line給的圖片id
        :return     1 : 成功 
                    0 : 失敗
        '''
        if img_id == 0:
            return 0
        file_name = self._save_img(img_id, content)
        update_pet("pet_photo", file_name, user_id, self.updateNum[user_id])
        return 1


def return_image_breed(url):
    '''
    回傳圖片品種辨識結果
    :param url : 圖片網址連結
    :return 品種
    '''
    params = {
        "engine": "google_lens",
        "url": url,
        "api_key": "7bec1da4ca2d934e97d542f96113cad7e2b7052e13098b7741416c75e8221073",
        "hl": "zh-tw"
    }
    request_url = "https://serpapi.com/search.json?engine=google_lens&url=" + url
    response = requests.get(request_url, data=params)
    response.encoding = "utf-8"
    content = response.json()
    try:
        breed = (content['knowledge_graph'][0])['title']
    except:
        breed = "未知"
    return breed


def is_dog(image_path):
    '''
    判斷是否為狗子
    :return 1 : 是
            0 : 否
    '''
    # 設定您的Google Cloud認證環境變數
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./zhengtian-488e92363e42.json"
    # 建立Vision API客戶端
    client = vision_v1.ImageAnnotatorClient()
    # 讀取本地圖片文件
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    # 建立Image類型的protobuf對象
    image = types.Image(content=content)
    # 使用Vision API進行圖像搜尋
    response = client.label_detection(image=image)
    labels = response.label_annotations
    # 過濾出狗的品種
    for label in labels:
        if label.description == "Dog breed":
            return 1
    return 0
