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

# if cursor.fetchall() find nothing return () -> empty tuple
# cursor.fetchall() find data return ([])  -> list in tuple


def execute_sql(sql, args=None):
    # used for SELECT method
    db = connect_database()
    cursor = db.cursor()
    try:
        with cursor:
            cursor.execute(sql, args)
            db.commit()
            # return match data
            return cursor.fetchall()
    except Exception as e:
        db.rollback()
    finally:
        cursor.close()  # turn off cursor
        db.close()


def execute_sql_2(sql, args=None):
    # used for INSERT, UPDATE, DELETE method
    db = connect_database()
    cursor = db.cursor()
    try:
        with cursor:
            cursor.execute(sql, args)
            db.commit()
            # return number of changed data
            return cursor.rowcount
    except Exception as e:
        db.rollback()
        return 0
    finally:
        cursor.close()
        db.close()


def user_id_exists(user_id):
    # 每次使用者傳訊息皆須判斷
    # Check if user_id exists in the database
    sql = 'SELECT * FROM `user` WHERE `user_id` = %s'
    try:
        result = execute_sql(sql, (user_id,))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")

    if result:
        print("資料已存在DB")
    else:
        sql = 'INSERT INTO `user` (`user_id`) VALUES (%s)'
        try:
            result_insert = execute_sql_2(sql, (user_id,))
        except Exception as e:
            print(f"SQL 錯誤: {str(e)}")

        if result_insert > 0:
            print("加入成功")
        else:
            print("加入失敗")


def append_pet(user_id, pet_name, pet_photo, pet_breed):
    # check if the pet already exists
    sql = 'SELECT `user_id`, `pet_name` FROM `pet` WHERE `user_id` = %s AND `pet_name` = %s'
    try:
        result = execute_sql(sql, (user_id, pet_name))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
        return False

    if result:
        print("寵物名稱重複")
        return ("寵物名稱重複")
    else:
        sql = 'INSERT INTO  `pet`(`user_id`, `pet_name`, `pet_photo`, `pet_breed`) VALUES (%s , %s , %s , %s)'
        try:
            result_insert = execute_sql_2(
                sql, (user_id, pet_name, pet_photo, pet_breed))
        except Exception as e:
            print(f"SQL 錯誤: {str(e)}")
            return False

        if result_insert > 0:
            print("新增成功")
            return ("新增成功")
        else:
            print("新增失敗")
            return ("新增失敗")


def revise_pet(user_id, pet_name, pet_photo, pet_breed, origin_name):
    sql = 'UPDATE `pet` SET `pet_name`= %s ,`pet_photo`= %s ,`pet_breed`= %s WHERE (`user_id` = %s) AND (`pet_name` = %s)'
    # for testing
    # get originl pet_name from json
    try:
        result_update = execute_sql_2(
            sql, (pet_name, pet_photo, pet_breed, user_id, origin_name))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
        return False
    if result_update > 0:
        print("更新成功")
        return ("更新成功")
    else:
        print("更新失敗")
        return ("更新失敗")


def delete_pet(user_id, pet_name):
    # delete data in `emotion_record` table
    sql2 = 'DELETE FROM `emotion_record` WHERE `pet_id` IN (SELECT `pet_id` FROM `pet` WHERE `user_id` = %s AND pet_name = %s)'
    try:
        execute_sql_2(sql2, (user_id, pet_name))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
        return False
    # delete data in `pet` table
    sql = 'DELETE FROM `pet` WHERE `user_id` = %s AND `pet_name` = %s'
    try:
        result_delete_pet = execute_sql_2(sql, (user_id, pet_name))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
        return False

    if result_delete_pet > 0:
        print("刪除成功")
        return ("刪除成功")
    else:
        print("刪除失敗")
        return ("刪除失敗")


def find_pet_id(user_id, pet_name):
    sql = 'SELECT `user_id`, `pet_name` , `pet_id` FROM `pet` WHERE `user_id` = %s AND `pet_name` = %s'
    try:
        result = execute_sql(sql, (user_id, pet_name))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
    if result:
        # get pet_id in return tuple
        pet_id = result[0][2]
        print(pet_id)
        return int(pet_id)
    else:
        return None


def append_emotion(emotion_photo, emotion, user_id, pet_name):
    sql = 'INSERT INTO  `emotion_record` (`pet_id`, `emotion_photo`, `emotion`) VALUES (%s , %s , %s)'
    try:
        result = execute_sql_2(
            sql, (find_pet_id(user_id, pet_name), emotion_photo, emotion))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
        return False

    if result > 0:
        print("新增分析結果成功")
        return("新增分析結果成功")
    else:
        print("新增分析結果失敗")
        return("新增分析結果失敗")


def show_all_pet(user_id):
    sql = 'SELECT `pet_id` FROM `pet` WHERE `user_id` = %s'
    try:
        # result return a tuple
        result_pet = execute_sql(sql, (user_id))
    except Exception as e:
        print(f"SQL 錯誤: {str(e)}")
        return False
    if result_pet:
        sql = 'SELECT * FROM `emotion_record` WHERE `pet_id` IN (SELECT `pet_id` FROM `pet` WHERE `user_id` = %s)'
        try:
            # result return a tuple
            result_emotion = execute_sql(sql, (user_id))
            pet_list = []
        except Exception as e:
            print(f"SQL 錯誤: {str(e)}")
            return False
        if result_emotion:
            # switch tuple to dict
            for row in result_emotion:
                pet_dict = {
                    'pet_id': row[0],
                    'emotion_photo': row[1],
                    'emotion': row[2],
                    'updated_time': row[3]
                }
            pet_list.append(pet_dict)
            print(pet_list)
            return("顯示寵物資料")
        else:
            print("尚無寵物情情緒分析結果！")
            return("尚無寵物情情緒分析結果！")
    else:
        print("尚無添加寵物")
        return("尚無添加寵物")


# user_id_exists('6')
# user_id_exists('188')
# append_pet('KIOLLLL', 'lol', '5678.png', '大胖狗')
# revise_pet('KIOLLLL', 'Oreo2', 'okok.png', '大麥町', 'Oreo')
# delete_pet('KIOLLLL', 'bb')
# find_pet_id('U751dd717d052680824fd250ddb7a7a55', 'Golden')
# append_emotion('relaxed.jpg', '放鬆',
#                'U751dd717d052680824fd250ddb7a7a55', 'Golden')
# show_all_pet('U751dd717d052680824fd250ddb7a7a55')
# show_all_pet('KIOLLLL')
