import flask
from flask import jsonify, request
from flask_cors import CORS
import pymysql


server = flask.Flask(__name__)
server.config["JSON_AS_ASCII"] = False
server.config["DEBUG"] = True
# 跨網域請求CORS(app, resources={r"./*":{"origins":["http://127.0.0.1:5500","*"]}})
CORS(server, resources={r"./*": {"origins": ["http://127.0.0.1:5000", "*"]}})


db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='linebot_project',
    charset='utf8mb4'
)

cursor = db.cursor()  # 連線後的游標


# test
# @server.route('/db/user', methods=['GET'])
# def users():
#     res = {"success": False, "info": "查詢失敗"}
#     try:
#         if request.method == 'GET':
#             sql = "SELECT * FROM `user`"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             res['info'] = '查詢成功'
#             res['success'] = True
#             res['results'] = result
#     except Exception as e:
#         db.rollback()
#         res['info'] = f'SQL 執行失敗: {e}'
#     return jsonify(res)

# @server.route('/db/user', methods=['GET'])
def user_id_exists(user_id):
    res = {"success": False, "info": "查詢失敗"}
    try:
        # with cursor:
        # Check if user_id exists in the database
        sql = 'SELECT * FROM `user` WHERE `user_id` = %s'
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        print(result)
        # if cursor.fetchall() find nothing return () -> empty tuple
        if result and isinstance(result, list) and len(result) > 0:
            print(result)
        elif isinstance(result, tuple) and len(result) == 0:
            # If user_id does not exist, insert a new row into the database
            sql = 'INSERT INTO `user` (`user_id`) VALUES (%s)'
            cursor.execute(sql, (user_id,))
            db.commit()
            print(result)
            # test whether the userid is insert into database successfully
            cursor.execute(
                "SHOW KEYS FROM table_name WHERE Key_name = 'PRIMARY'")
            result_set = cursor.fetchall()
            if result_set:
                # insert success
                print("資料表存在primary key")
            else:
                # insert failed
                print("資料表不存在primary key")

    except Exception as e:
        db.rollback()
        print(f'SQL 執行失敗: {e}')
    finally:
        cursor.close()  # turn off cursor
        db.close()
        print('finally')


if __name__ == "__main__":
    server.run(port=5000)
