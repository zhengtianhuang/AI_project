# app.py
'''
引用庫
'''
from handler import handler
import os
from pathlib import Path
from json import load, dump
from linebot.exceptions import (
    InvalidSignatureError
)
from flask import Flask, request, abort, render_template, url_for
'''
變數區
'''
app = Flask(__name__)
bubblePath = Path(__file__).resolve().parent/'static/json/bubbles'
'''
主程式
'''


@app.route("/test", methods=['GET'])
def test():
    return "ok"


@app.route("/", methods=['GET'])
def print_img():
    image_url = url_for('static', filename='img/cant_see.png')
    return render_template("cant_see.html", image_url=image_url)


@ app.route("/callback", methods=['POST'])
def callback():
    '''
    處理linebot伺服器回傳data
    '''
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def initial():
    '''
    只需一開始執行一次
    '''

    restaurant_bubble = load(
        open(f'{bubblePath}/restaurant.json', 'r', encoding='utf-8'))
    pet_bubble = load(open(f'{bubblePath}/pet.json', 'r', encoding='utf-8'))
    restaurant_bubble["hero"]["action"]["uri"] = os.getenv("WEBHOOK_URL")
    restaurant_bubble["footer"]["contents"][0]["action"]["uri"] = os.getenv(
        "WEBHOOK_URL")
    pet_bubble["hero"]["action"]["uri"] = os.getenv("WEBHOOK_URL")
    # 寫回 JSON 檔案
    with open(f'{bubblePath}/restaurant.json', 'w') as f:
        dump(restaurant_bubble, f)
    # 寫回 JSON 檔案
    with open(f'{bubblePath}/pet.json', 'w') as f:
        dump(pet_bubble, f)


if __name__ == "__main__":
    initial()
    app.run(port=8080, debug=True)
