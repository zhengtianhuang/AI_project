import pymysql


def connect_database():
    '''
    連接sql資料庫
    '''
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='linebot_project',
        charset='utf8mb4'
    )
    return db


def append_user(user_id):
    '''
    確認此user_id是否存在資料庫, 若沒有, 則新增此id
    :param user_id : linebot用戶id
    '''
    db = connect_database()
    cursor = db.cursor()  # 連線後的游標
    try:
        with cursor:
            sql = 'SELECT * FROM `users` WHERE `user_id` = %s'
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            if result and isinstance(result, tuple) and len(result) > 0:
                print("資料已存在DB")
            elif isinstance(result, tuple) and len(result) == 0:
                sql = 'INSERT INTO `users` (`user_id`) VALUES (%s)'
                cursor.execute(sql, (user_id,))
                db.commit()
                cursor.execute(
                    "SHOW KEYS FROM `users` WHERE Key_name = 'PRIMARY'")
                result_set = cursor.fetchall()
                if result_set:
                    print("資料加入DB成功")
                else:
                    print("資料加入DB失敗")
    except Exception as e:
        db.rollback()
        print(f'SQL 執行失敗: {e}')
    finally:
        cursor.close()
        db.close()


def append_pet(user_id, pet_name, pet_photo, pet_breed):
    '''
    將寵物資料存進資料庫
    :param userid : linebot用戶id
    '''
    db = connect_database()
    cursor = db.cursor()  # 連線後的游標
    try:
        with cursor:
            sql = 'SELECT `user_id`, `pet_name`,`pet_breed` FROM `pets` WHERE `user_id` = %s AND `pet_name` = %s AND `pet_breed` = %s'
            cursor.execute(sql, (user_id, pet_name, pet_breed))
            result = cursor.fetchall()
            print(result)
            if result and isinstance(result, tuple) and len(result) > 0:
                print("資料已存在DB")
            elif isinstance(result, tuple) and len(result) == 0:
                sql = 'INSERT INTO `pets`(`user_id`, `pet_name`, `pet_photo`, `pet_breed`) VALUES (%s , %s , %s , %s)'
                cursor.execute(sql, (user_id, pet_name, pet_photo, pet_breed))
                db.commit()
                print("資料加入DB成功")
    except Exception as e:
        db.rollback()
        print(f'SQL 執行失敗: {e}')
    finally:
        cursor.close()
        db.close()


def search_pet(user_id):
    '''
    搜尋寵物資料
    :param user_id : linebot用戶id
    :param num :  第幾隻寵物
    '''
    db = connect_database()
    cursor = db.cursor()
    query = "SELECT `pet_name`, `pet_photo`, `pet_breed` FROM pets WHERE user_id = %s"
    cursor.execute(query, (user_id))
    result = cursor.fetchall()
    for row in result:
        print("Pet name: {}, photo: {}, breed: {}".format(
            row[0], row[1], row[2]))
    cursor.close()
    db.close()
    return result


def update_pet(column_name, data, user_id, num):
    '''
    更新寵物資料
    :param user_id : linebot用戶id
    :param num :  第幾隻寵物
    '''
    db = connect_database()
    cursor = db.cursor()
    query = "UPDATE pets SET {}=%s WHERE pet_id=(SELECT pet_id FROM pets WHERE user_id = %s LIMIT 1 OFFSET %s)".format(
        column_name)
    cursor.execute(query, (data, user_id, num))
    db.commit()
    cursor.close()
    db.close()


def delete_pet(user_id, num):
    '''
    刪除寵物資料
    :param user_id : linebot用戶id
    :param num :  第幾隻寵物
    '''
    db = connect_database()
    cursor = db.cursor()
    query = "DELETE FROM pets WHERE pet_id=(SELECT pet_id FROM pets WHERE user_id = %s LIMIT 1 OFFSET %s)"
    cursor.execute(query, (user_id, num))
    db.commit()
    cursor.close()
    db.close()
