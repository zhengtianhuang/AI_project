# app.py
'''
引用庫
'''
from flask import Flask, request, abort, render_template, url_for
from linebot.exceptions import (
    InvalidSignatureError
)
# =============副程式==================
from handler import handler
'''
變數區
'''
app = Flask(__name__)
'''
主程式
'''


@app.route("/test", methods=['GET'])
def test():
    return "ok"


@app.route("/notfound", methods=['GET'])
def print_img():
    image_url = url_for('static', filename='img/no_data.png')
    return render_template("no_data.html", image_url=image_url)


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


if __name__ == "__main__":
    app.run(port=8080, debug=True)
