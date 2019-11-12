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

    def delete_client(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM CLIENTS WHERE ID ='"+id+"'"
            cur.execute(sql)

    def add_client(self, name, surname, patronymic, phone):
        with self.__con:
            cur = self.__con.cursor()
            data = [name, surname, patronymic, phone]
            sql = 'INSERT INTO CLIENTS (name, surname, patronymic, phone) VALUES(%s, %s, %s, %s)'
            cur.execute(sql, data)

    def show_cars(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "SELECT * FROM cars WHERE ID_OWNER ='" + id + "'"
            cur.execute(sql)
            data = cur.fetchall()
            return data

    def delete_car(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM CARS WHERE CAR_NUMBER ='" + id + "'"
            cur.execute(sql)

    def add_car(self, number, id, mark, issue_date):
        with self.__con:
            cur = self.__con.cursor()
            data = [number, id, mark, issue_date]
            sql = 'INSERT INTO CARS (CAR_NUMBER, ID_OWNER, MODEL, ISSUE_DATE) VALUES(%s, %s, %s, %s)'
            cur.execute(sql, data)


