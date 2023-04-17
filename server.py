import pymysql


def user_id_exists(user_id):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='linebot_project',
        charset='utf8mb4'
    )
    cursor = db.cursor()  # 連線後的游標
    try:
        with cursor:
            # Check if user_id exists in the database
            sql = 'SELECT * FROM `user` WHERE `user_id` = %s'
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            # if cursor.fetchall() find nothing return () -> empty tuple
            if result and isinstance(result, list) and len(result) > 0:
                pass
            elif isinstance(result, tuple) and len(result) == 0:
                # If user_id does not exist, insert a new row into the database
                sql = 'INSERT INTO `user` (`user_id`) VALUES (%s)'
                cursor.execute(sql, (user_id,))
                db.commit()
                # test whether the userid is insert into database successfully
                cursor.execute(
                    "SHOW KEYS FROM `user` WHERE Key_name = 'PRIMARY'")
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


# user_id_exists('cde345')
