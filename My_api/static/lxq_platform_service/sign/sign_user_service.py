"""
_*_ coding: UTF-8 _*_
@Time      : 2021/3/5 15:46
@Author    : LiuXiaoQiang
@Site      : https://github.com/qq183727918
@File      : sign_user_service.py
@Software  : PyCharm
"""
import pymysql
from icecream import ic


def service_login(IDS):
    global ren
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user="root",
        password="root",
        database="automatedtest"
    )

    try:
        cursor = db.cursor()
        sql = f"SELECT * FROM login_user where username = '{IDS['user']}' AND password = '{IDS['pwd']}' AND is_delete = 0;"
        ic(sql)
        # 以数组的形式填充数据
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        ic(data)
        ren = {"code": 200, "data": "true", "message": data}
    except Exception as e:
        # 事务回滚
        db.rollback()
        ren = e
        ic(e)
    db.close()
    return ren


if __name__ == '__main__':
    IDS = {
        'user': '183727918',
        'pwd': '123456'
    }
    service_login(IDS)
