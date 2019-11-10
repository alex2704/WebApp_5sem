import pymysql
from pymysql.cursors import DictCursor


class DB:
    def __init__(self):
        self.__con = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='car_service',
            charset='utf8mb4',
            cursorclass=DictCursor)

    def get_clients(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM clients c')
            result = cur.fetchall()
            return result

