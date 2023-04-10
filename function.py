from json import load

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


def spider(a, b):
    # 這裡給經緯度要回傳兩個長度為5的list參數(景點名稱和圖片連結)
    return "兩個list"
