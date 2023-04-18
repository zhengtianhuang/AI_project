from json import load


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
