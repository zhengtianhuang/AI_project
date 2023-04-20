import pymysql
from datetime import datetime


def connect_database():
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='linebot_project',
        charset='utf8mb4'
    )
    return db


def now_datetime():
    now = datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def user_id_exists(user_id):
    db = connect_database()
    cursor = db.cursor()  # 連線後的游標
    try:
        with cursor:
            # Check if user_id exists in the database
            sql = 'SELECT * FROM `users` WHERE `user_id` = %s'
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            # if cursor.fetchall() find nothing return () -> empty tuple
            if result and isinstance(result, tuple) and len(result) > 0:
                print("資料已存在DB")
            elif isinstance(result, tuple) and len(result) == 0:
                # If user_id does not exist, insert a new row into the database
                sql = 'INSERT INTO `users` (`user_id`) VALUES (%s)'
                cursor.execute(sql, (user_id,))
                db.commit()
                # test whether the userid is insert into database successfully
                cursor.execute(
                    "SHOW KEYS FROM `users` WHERE Key_name = 'PRIMARY'")
                result_set = cursor.fetchall()
                if result_set:
                    # insert success
                    print("資料加入DB成功")
                else:
                    # insert failed
                    print("資料加入DB失敗")
    except Exception as e:
        db.rollback()
        print(f'SQL 執行失敗: {e}')
    finally:
        cursor.close()  # turn off cursor
        db.close()


def append_pet(user_id, pet_name, pet_photo, pet_breed):
    db = connect_database()
    cursor = db.cursor()  # 連線後的游標
    try:
        with cursor:
            # check whether data exists in database
            sql = 'SELECT `user_id`, `pet_name`,`pet_breed` FROM `pets` WHERE `user_id` = %s AND `pet_name` = %s AND `pet_breed` = %s'
            cursor.execute(sql, (user_id, pet_name, pet_breed))
            result = cursor.fetchall()
            print(result)
            # if cursor.fetchall() find nothing return () -> empty tuple
            if result and isinstance(result, tuple) and len(result) > 0:
                print("資料已存在DB")
            elif isinstance(result, tuple) and len(result) == 0:
                # If user_id does not exist, insert a new row into the database
                sql = 'INSERT INTO `pets`(`user_id`, `pet_name`, `pet_photo`, `pet_breed`) VALUES (%s , %s , %s , %s)'
                cursor.execute(sql, (user_id, pet_name, pet_photo, pet_breed))
                db.commit()
                print("資料加入DB成功")
    except Exception as e:
        db.rollback()
        print(f'SQL 執行失敗: {e}')
    finally:
        cursor.close()  # turn off cursor
        db.close()


def search_pet(user_id):
    db = connect_database()
    # 連線後的游標
    cursor = db.cursor()
    # 按用户ID查询宠物信息
    query = "SELECT `pet_name`, `pet_photo`, `pet_breed` FROM pets WHERE user_id = %s"
    cursor.execute(query, (user_id))
    # 获取查询结果
    result = cursor.fetchall()
    # 输出查询结果
    for row in result:
        print("Pet name: {}, photo: {}, breed: {}".format(
            row[0], row[1], row[2]))
    # 关闭数据库连接
    cursor.close()
    db.close()
    return result


def update_pet(column_name, data, user_id, num):
    db = connect_database()
    cursor = db.cursor()
    query = "UPDATE pets SET {}=%s WHERE pet_id=(SELECT pet_id FROM pets WHERE user_id = %s LIMIT 1 OFFSET %s)".format(
        column_name)
    cursor.execute(query, (data, user_id, num))

    db.commit()  # 提交事务

    cursor.close()
    db.close()


update_pet("pet_name", "piggy", '123', 1)
