# utils.py
'''
引用庫
'''
import requests
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import time
from datetime import datetime
from pathlib import Path
import os
import json
from database import db_update_pet, db_insert_pet_if_not_exist, db_insert_user_if_not_exist
'''
變數區
'''
static_path = Path(__file__).resolve().parent/'static'
'''
函式區
'''


""" def return_pet_restaurants(latitude, longitude):
    '''
    使用 Google Maps API 找尋指定經緯度附近的寵物餐廳。
    :param latitude (float) : 緯度。
    :param longitude (float) : 經度。
    :return list : 包含附近寵物餐廳資訊的字典列表。
                   每個字典包含以下欄位：
                    - resPhoto (str): 餐廳照片的 URL。
                    - resName (str): 餐廳名稱。
                    - resRating (float): 餐廳評分。
                    - resAdd (str): 餐廳地址。
                    - resOpen (str): 餐廳營業狀態，值為 "營業中" 或 "目前無營業"。
    '''
    res_info_all = []  # 存放所有找到的寵物餐廳資訊
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    types = "pet_store,veterinary_care"
    keyword = "寵物餐廳"
    radius = str(500)  # 範圍
    res_photo_prfx = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400"
    query_url = f"{url}location={latitude},{longitude}&radius={radius}&types={types}&keyword={keyword}&key={api_key}&language=zh-TW"
    response = requests.get(query_url)
    res = response.json()
    if res["status"] == "OK":
        results = res["results"]
        for result in results:
            res_info = {}
            # 取得餐廳照片的 URL
            photo_reference = result.get('photos', [{}])[
                0].get('photo_reference', '')
            res_info['resPhoto'] = f"{res_photo_prfx}&photo_reference={photo_reference}&key={api_key}"
            # 取得餐廳名稱、評分、地址
            res_info['resName'] = result.get("name", "")
            res_info['resRating'] = result.get("rating", 0)
            res_info['resAdd'] = f"{result.get('plus_code', {}).get('compound_code', '')[-3:]}{result.get('vicinity', '')}"
            # 取得餐廳營業狀態
            if result.get("opening_hours", {}).get("open_now", False):
                res_info['resOpen'] = "營業中"
            else:
                res_info['resOpen'] = "目前無營業"
            res_info_all.append(res_info)
    else:
        print("Request failed.")
    return res_info_all """

def return_pet_hospitals(latitude, longitude):
    '''
    使用 Google Maps API 找尋指定經緯度附近的寵物醫院。
    :param latitude (float) : 緯度。
    :param longitude (float) : 經度。
    :return list : 包含附近寵物醫院資訊的字典列表。
                   每個字典包含以下欄位：
                    - hospitalPhoto (str): 醫院照片的 URL。
                    - hospitalName (str): 醫院名稱。
                    - hospitalRating (float): 醫院評分。
                    - hospitalAdd (str): 醫院地址。
                    - hospitalOpen (str): 醫院營業狀態，值為 "營業中" 或 "目前無營業"。
    '''
    hospital_info_all = []  # 存放所有找到的寵物醫院資訊
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    types = "veterinary_care"  # Specify the type as veterinary_care to get pet hospitals
    keyword = "寵物醫院"  # Specify the keyword as pet hospital
    radius = str(500)  # 範圍
    hospital_photo_prfx = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400"
    query_url = f"{url}location={latitude},{longitude}&radius={radius}&types={types}&keyword={keyword}&key={api_key}&language=zh-TW"
    response = requests.get(query_url)
    res = response.json()
    if res["status"] == "OK":
        results = res["results"]
        for result in results:
            hospital_info = {}
            # 取得醫院照片的 URL
            photo_reference = result.get('photos', [{}])[0].get('photo_reference', '')
            hospital_info['hospitalPhoto'] = f"{hospital_photo_prfx}&photo_reference={photo_reference}&key={api_key}"
            # 取得醫院名稱、評分、地址
            hospital_info['hospitalName'] = result.get("name", "")
            hospital_info['hospitalRating'] = result.get("rating", 0)
            hospital_info['hospitalAdd'] = f"{result.get('plus_code', {}).get('compound_code', '')[-3:]}{result.get('vicinity', '')}"
            # 取得醫院營業狀態
            if result.get("opening_hours", {}).get("open_now", False):
                hospital_info['hospitalOpen'] = "營業中"
            else:
                hospital_info['hospitalOpen'] = "目前無營業"
            hospital_info_all.append(hospital_info)
    else:
        print("Request failed.")
    return hospital_info_all



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
                return "照片更新成功！"
            return "這不是圖片！"
        elif self.updateCol[user_id] == 2:  # 用戶按下更改名字
            col_name = "pet_name"
        elif self.updateCol[user_id] == 3:  # 用戶按下更改品種
            col_name = "pet_breed"
        db_update_pet(col_name, data, user_id, self.updateNum[user_id])
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
        photo_path = os.path.join(static_path, 'pet_img', filename)
        with open(photo_path, 'wb') as f:
            for chunk in content.iter_content():
                f.write(chunk)
        return filename

    def delete_img(self, img_path):
        '''
        刪除圖片
        '''
        if os.path.isfile(img_path):
            os.remove(img_path)
            print("delete success")

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
            os.getenv('WEBHOOK_URL'), 'static/pet_img', file_name)
        self.breed[user_id] = return_image_breed(img_url)
        db_insert_user_if_not_exist(user_id)
        db_insert_pet_if_not_exist(user_id, self.name[user_id],
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
        db_update_pet("pet_photo", file_name, user_id, self.updateNum[user_id])
        return 1


def return_image_breed(url):
    '''
    回傳圖片品種辨識結果
    :param url : 圖片網址連結
    :return 品種
    '''
    # 轉換url成使用lens用法網址
    first_url = url.replace('/', '%2F')
    second_url = first_url.replace(':', '%3A')
    params = {
        "engine": "google_lens",
        "url": second_url,
        "api_key": str(os.getenv("GOOGLE_SEARCH_API_KEY")),
        "hl": "zh-tw"
    }
    request_url = "https://serpapi.com/search.json?engine=google_lens&url=" + second_url
    response = requests.get(request_url, data=params)
    response.encoding = "utf-8"
    content = response.json()
    print(content)
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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(Path(
        __file__).resolve().parent/"Secret/zhengtian-488e92363e42.json")
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


def delta_time(time):
    '''
    判斷資料更新時間過多久
    :param time : 要計算的時間(年-月-日 時:分:秒)
    :return 幾秒/幾分鐘/幾小時前/日期
    '''
    current_time = datetime.now()
    data_time = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')
    delta_time = current_time - data_time

    seconds = int(delta_time.total_seconds())
    minutes = int(seconds/60)
    hours = int(minutes/60)

    if seconds < 0:
        return 0
    elif seconds < 60:
        message = ("上次分析: " + str(seconds) + "秒鐘前")
        return message
    elif minutes < 60:
        message = ("上次分析: " + str(minutes) + "分鐘前")
        return message
    elif hours < 24:
        message = ("上次分析: " + str(hours) + "小時前")
        return message
    else:
        return data_time


""" def return_pet_restaurant_details(name):
    '''
    抓取google knowledge graph中的商家資訊

    :param name : 店家名字
    '''
    params = {
        "api_key": str(os.getenv("GOOGLE_SEARCH_API_KEY")),
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
    return response.json() """

def return_pet_hospital_details(name):
    '''
    抓取google knowledge graph中的商家資訊

    :param name : 店家名字
    '''
    params = {
        "api_key": str(os.getenv("GOOGLE_SEARCH_API_KEY")),
        "engine": "google",
        "q": name,
        "google_domain": "google.com.tw",
        "hl": "zh-tw",
        "gl": "tw",
        "tbs": "veterinary_care"  # Set tbs to veterinary_care for pet hospitals
    }
    request_url = "https://serpapi.com/search.json?engine=google&q=" + name
    response = requests.get(request_url, data=params)
    response.encoding = 'uft-8'
    return response.json()

    