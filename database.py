# database.py
'''
引用庫
'''
import pymysql
'''
函式區
'''


def connect_database(func):
    '''
    這是一個裝飾器，用來連接資料庫並處理 SQL 語句
    '''
    def wrapper(*args, **kwargs):
        db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='linebot_project',
            charset='utf8mb4'
        )
        result = None
        try:
            result = func(db, *args, **kwargs)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f'SQL 執行失敗: {e}')
        finally:
            db.close()
        return result
    return wrapper


@connect_database
def db_insert_user_if_not_exist(db, user_id):
    '''
    向資料庫的 `users` 表格中新增使用者資料，如果已經存在則不做任何操作。

    :param db: 資料庫連線物件
    :param user_id: linebot的用戶ID
    '''
    with db.cursor() as cursor:
        with db.cursor() as cursor:
            sql = 'INSERT INTO `users` (`user_id`) VALUES (%s) ON DUPLICATE KEY UPDATE `user_id` = `user_id`'
            cursor.execute(sql, (user_id,))
            if cursor.rowcount > 0:
                print("資料加入DB成功")
            else:
                print("資料已存在DB")


@connect_database
def db_insert_pet_if_not_exist(db, user_id, pet_name, pet_photo, pet_breed):
    """
    向資料庫的 `pets` 表格中新增寵物資料，如果已經存在則不做任何操作。

    :param db: 資料庫連線物件
    :param user_id: 寵物主人的linebot_id
    :param pet_name: 寵物名稱
    :param pet_photo: 寵物照片檔名
    :param pet_breed: 寵物品種
    """
    with db.cursor() as cursor:
        # 檢查該條紀錄是否已經存在
        sql = 'SELECT `user_id`, `pet_name`,`pet_breed` FROM `pets` WHERE `user_id` = %s AND `pet_name` = %s AND `pet_breed` = %s'
        cursor.execute(sql, (user_id, pet_name, pet_breed))
        result = cursor.fetchone()
        if result:
            print("資料已存在DB")
        else:
            # 插入新紀錄
            sql = 'INSERT INTO `pets`(`user_id`, `pet_name`, `pet_photo`, `pet_breed`) VALUES (%s , %s , %s , %s)'
            cursor.execute(sql, (user_id, pet_name, pet_photo, pet_breed))
            print("資料加入DB成功")


@connect_database
def db_search_pet(db, user_id):
    """
    連線資料庫並搜尋指定使用者的寵物資料。

    :param db: 資料庫連線物件。
    :param user_id: 要搜尋的使用者ID。

    :return tuple: 以tuple形式儲存的寵物資料, 若查無資料則為空tuple

            - pet_name
            - pet_photo
            - pet_breed
            - pet_id
    """
    with db.cursor() as cursor:
        query = "SELECT `pet_name`, `pet_photo`, `pet_breed`, `pet_id` FROM `pets` WHERE `user_id` = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        for row in result:
            print("Pet name: {}, photo: {}, breed: {}".format(
                row[0], row[1], row[2]))
    return result


@connect_database
def db_update_pet(db, column_name, data, user_id, num):
    """
    更新寵物資料表格中的特定欄位資料

    :param db: 資料庫連線
    :param column_name: 要更新的欄位名稱
    :param data: 要更新的資料
    :param user_id: 寵物所屬的使用者ID
    :param num: 要更新第幾個寵物資料
    """
    with db.cursor() as cursor:
        # 使用format方法將欄位名稱加入SQL指令中
        query = "UPDATE pets SET {}=%s WHERE pet_id=(SELECT pet_id FROM pets WHERE user_id = %s LIMIT 1 OFFSET %s)".format(
            column_name)
        # 使用execute方法執行SQL指令
        cursor.execute(query, (data, user_id, num))
        if cursor.rowcount > 0:
            print("更新成功")
        else:
            print("沒有任何資料被更新")


@connect_database
def db_delete_pet(db, user_id, num):
    '''
    刪除寵物資料

    :param user_id : linebot用戶id
    :param num :  第幾隻寵物(1開始)
    '''
    with db.cursor() as cursor:
        query = "DELETE FROM pets_emotions WHERE pet_id=(SELECT pet_id FROM pets WHERE user_id = %s)"
        cursor.execute(query, (user_id,))
        query = "DELETE FROM pets WHERE pet_id=(SELECT pet_id FROM pets WHERE user_id = %s LIMIT 1 OFFSET %s)"
        cursor.execute(query, (user_id, num))
        cursor.close()


@connect_database
def db_append_emotion(db, pet_id, pet_emotion):
    '''
    新增寵物情緒(資料庫只儲存最近一筆情緒分析情果)

    :param pet_id : pet在資料庫分配到的id(pet_id)
    :param pet_emotion :  分析情緒結果
    '''
    with db.cursor() as cursor:
        query = "SELECT * FROM `pets_emotions` WHERE `pet_id` = %s"
        cursor.execute(query, (pet_id))
        result = cursor.fetchone()
        if result:
            update = "UPDATE `pets_emotions` SET `pet_emotion`= %s WHERE `pet_id`= %s"
            cursor.execute(update, (pet_emotion, pet_id))
            if cursor.rowcount > 0:
                print("更新成功")
            else:
                print("沒有任何資料被更新")
        else:
            append = "INSERT INTO `pets_emotions`(`pet_id`, `pet_emotion`) VALUES (%s,%s)"
            cursor.execute(append, (pet_id, pet_emotion))
            if cursor.rowcount > 0:
                print("新增成功")
            else:
                print("沒有任何資料被更新")


@connect_database
def db_search_emotion(db, pet_id):
    '''
    搜尋寵物情緒

    :param pet_id : pet在資料庫分配到的id(get_id)
    :return result : 無資料時 
                        - 0
                     有資料
                        - pet-emotion
                        - update-time
    '''
    with db.cursor() as cursor:
        query = "SELECT `pet_emotion`, `updated_time` FROM `pets_emotions` WHERE `pet_id` = %s"
        cursor.execute(query, (pet_id))
        result = cursor.fetchone()
        if result:  # 有情緒分析資料
            return result
        # 無情緒分析資料
        return 0
