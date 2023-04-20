from json import load
from pathlib import Path
bubblePath = Path(__file__).resolve().parent/'static/json/bubbles'


class templates():
    def __init__(self):
        self.template = {
            "type": "carousel",
            "contents": []
        }
        self.tCount = 0

    def add_restaurant_bubble(self, image, name, rating, add, isOpen):
        bubble = load(
            open(f'{bubblePath}/restaurantBubble.json', 'r', encoding='utf-8'))
        # print(bubble)
        bubble["hero"]["url"] = str(image)
        bubble["body"]["contents"][0]["text"] = str(name)
        bubble["body"]["contents"][1]["contents"][5]["text"] = str(rating)
        bubble["body"]["contents"][3]["contents"][1]["text"] = str(add)
        bubble["body"]["contents"][4]["contents"][1]["text"] = str(isOpen)
        self.template["contents"].append(bubble)

    def add_pet_bubble(self, image, name, breed, emo, time):
        bubble = load(
            open(f'{bubblePath}/pet.json', 'r', encoding='utf-8'))
        # print(bubble)
        bubble["hero"]["url"] = str(image)
        bubble["body"]["contents"][0]["text"] = str(name)
        bubble["body"]["contents"][1]["contents"][0]["contents"][2]["text"] = str(
            breed)
        bubble["body"]["contents"][1]["contents"][1]["contents"][2]["text"] = str(
            emo)
        bubble["body"]["contents"][2]["text"] = str(time)

        bubble["footer"]["contents"][0]["action"]["data"] = f"{self.tCount}更改照片"
        bubble["footer"]["contents"][1]["action"]["data"] = f"{self.tCount}更改名字"
        bubble["footer"]["contents"][2]["action"]["data"] = f"{self.tCount}更改品種"
        bubble["footer"]["contents"][3]["action"]["data"] = f"{self.tCount}刪除"

        self.template["contents"].append(bubble)
