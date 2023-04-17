import requests

# 設置欲上傳的圖片路徑
img_path = "./side_projects/richmenu/richmenu.png"


# 1. 創建 Rich Menu，指定剛剛上傳的圖片的 contentId，獲取 richmenu id
url = "https://api.line.me/v2/bot/richmenu"
headers = {
    "Authorization": "Bearer 80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU=",
    "Content-Type": "application/json"
}
data = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": "true",
    "name": "圖文選單 1",
    "chatBarText": "查看更多資訊",
    "areas": [
        {
            "bounds": {
                "x": 172,
                "y": 625,
                "width": 618,
                "height": 409
            },
            "action": {
                "type": "postback",
                "text": "功能介紹",
                "data": "功能介紹"
            }
        },
        {
            "bounds": {
                "x": 1717,
                "y": 621,
                "width": 614,
                "height": 435
            },
            "action": {
                "type": "postback",
                "text": "寵物資料",
                "data": "寵物資料"
            }
        },
        {
            "bounds": {
                "x": 165,
                "y": 1070,
                "width": 625,
                "height": 521
            },
            "action": {
                "type": "postback",
                "text": "寵物情緒分析",
                "data": "寵物情緒分析"
            }
        },
        {
            "bounds": {
                "x": 1724,
                "y": 1074,
                "width": 596,
                "height": 510
            },
            "action": {
                "type": "postback",
                "text": "新增資料",
                "data": "新增資料"
            }
        }
    ]
}
response = requests.post(url, headers=headers, json=data)
richmenu_id = response.json()["richMenuId"]
print(f"number1{richmenu_id}")

# 2. 上傳 Rich Menu 圖片
url = f"https://api-data.line.me/v2/bot/richmenu/{richmenu_id}/content"
headers = {
    "Authorization": "Bearer 80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU=",
    "Content-Type": "image/png"
}
response = requests.post(url, headers=headers, data=open(img_path, "rb"))
print(f"number2{response}")
# 3. 設置預設的 Rich Menu
url = "https://api.line.me/v2/bot/user/all/richmenu/{}".format(richmenu_id)
headers = {
    "Authorization": "Bearer 80rOecVLLMFyO6yOiljvHWK2UA6Nsq02z2dssrX0Ch0loc1s0byACoyHn1gMLHdGLnMvinAd8zJUkg2zXYkxF6EE35G2rN/cRDXuUQpOIGhRjjeKXM9RRVQR5evVpVS/5O3Nqc2Q/9bCYdXwo20C+gdB04t89/1O/w1cDnyilFU="
}
response = requests.post(url, headers=headers)
print(f"number3{response}")
