import flask
from flask import jsonify, request
from flask_cors import CORS
import pymysql

app = flask.Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["DEBUG"] = True
# 跨網域請求CORS(app, resources={r"./*":{"origins":["http://127.0.0.1:5500","*"]}})
CORS(app, resources={r"./*": {"origins": ["http://127.0.0.1:5000", "*"]}})


db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='linebot_project',
    charset='utf8mb4'
)

cursor = db.cursor()  # 連線後的游標


@app.route('/test', methods=['GET'])
def home():
    return "<h1>Welecome to my flask server.</h1>"


@app.route('/db/user', methods=['GET'])
def studnets():
    res = {"success": False, "info": "查詢失敗"}
    try:
        if request.method == 'GET':
            sql = "SELECT * FROM `user`"
            cursor.execute(sql)
            result = cursor.fetchall()
            res['info'] = '查詢成功'
            res['success'] = True
            res['results'] = result
    except Exception as e:
        db.rollback()
        res['info'] = f'SQL 執行失敗: {e}'
    return jsonify(res)


app.run()
