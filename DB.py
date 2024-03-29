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

    def add_user(self, name, password):
        with self.__con:
            cur = self.__con.cursor()
            data = (name, password, 0)
            cur.execute('INSERT into users (username, password, rules) VALUES (%s, %s, %s)', data)

    def login(self, name, password):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT * FROM users WHERE username=%s', (name,))
            user = cur.fetchone()
            return user

    def get_priveleges(self, name):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT * FROM users WHERE username=%s', (name,))
            user = cur.fetchone()
            result = user['rules']
            return result

    def get_clients(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM clients c')
            result = cur.fetchall()
            return result

    def search_client(self, surname):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM clients c WHERE surname = %s', (surname, ))
            result = cur.fetchall()
            return result

    def search_client_n(self, name, patronymic):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM clients c WHERE name = %s and patronymic = %s', (name, patronymic))
            result = cur.fetchall()
            return result

    def delete_client(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM CLIENTS WHERE ID = %s"
            cur.execute(sql, (id ,))

    def add_client(self, name, surname, patronymic, phone):
        with self.__con:
            cur = self.__con.cursor()
            data = [name, surname, patronymic, phone]
            sql = 'INSERT INTO CLIENTS (name, surname, patronymic, phone) VALUES(%s, %s, %s, %s)'
            cur.execute(sql, data)

    def show_cars(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "SELECT * FROM cars WHERE ID_OWNER = %s"
            cur.execute(sql, (id, ))
            data = cur.fetchall()
            return data

    def delete_car(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM CARS WHERE CAR_NUMBER = %s"
            cur.execute(sql, (id,))

    def add_car(self, number, id, mark, issue_date):
        with self.__con:
            cur = self.__con.cursor()
            data = [number, id, mark, issue_date]
            sql = 'INSERT INTO CARS (CAR_NUMBER, ID_OWNER, MODEL, ISSUE_DATE) VALUES(%s, %s, %s, %s)'
            cur.execute(sql, data)

    def get_employees(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT e.* FROM employees e')
            result = cur.fetchall()
            return result

    def get_all_cars(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM cars c')
            result = cur.fetchall()
            return result

    def delete_employee(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM EMPLOYEES WHERE ID = %s"
            cur.execute(sql, (id ,))

    def add_employee(self, name, surname, patronymic, birth_date, address, phone, id_position, work_time, prize):
        with self.__con:
            cur = self.__con.cursor()
            data = [name, surname, patronymic, birth_date, address, phone, id_position, work_time, prize]
            sql = 'INSERT INTO employees (name, surname, patronymic, birth_date, address, phone_number, id_position, work_time, prize) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cur.execute(sql, data)

    # изменить значение ячейки
    def change_value(self, table, cell, value, name_identificator, identificator):
        with self.__con:
            cur = self.__con.cursor()
            sql = "UPDATE " + table + " SET " + cell + "= %s WHERE " + name_identificator + " = %s"
            val = (value, identificator)
            cur.execute(sql, val)

    def get_value(self, table, name_identificator, identificator):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT * FROM ' + table + ' WHERE ' + name_identificator + " = %s", (identificator, ))
            result = cur.fetchall()
            return result

    # POSITION
    def get_all_positions(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT p.* FROM position p')
            result = cur.fetchall()
            return result

    def add_position(self, position, salary):
        with self.__con:
            cur = self.__con.cursor()
            data = [position, salary]
            sql = 'INSERT INTO position (position, salary) VALUES(%s, %s)'
            cur.execute(sql, data)

    def show_positions(self):
        with self.__con:
            cur = self.__con.cursor()
            sql = "SELECT * FROM position"
            cur.execute(sql)
            data = cur.fetchall()
            return data

    def delete_position(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM position WHERE ID = %s "
            cur.execute(sql, (id ,))

    #   APPEALS
    def show_appeals(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT a.* FROM appeals a')
            result = cur.fetchall()
            return result

    def add_appeal(self, car_number, fault):
        with self.__con:
            cur = self.__con.cursor()
            data = [car_number, fault]
            sql = 'INSERT INTO appeals (car_number, fault) VALUES(%s, %s)'
            cur.execute(sql, data)

    def delete_appeal(self, id):
        with self.__con:
            cur = self.__con.cursor()
            sql = "DELETE FROM appeals WHERE appeal_number = %s"
            cur.execute(sql, (id, ))

    def get_appeal_car(self, number):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM appeals c WHERE car_number= %s', (number, ))
            result = cur.fetchall()
            return result

    def get_repair_works(self, appeal_number):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM repair_works c WHERE appeal_number= %s', (appeal_number, ))
            result = cur.fetchall()
            return result

    def get_all_appeals(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT a.* FROM appeals a')
            result = cur.fetchall()
            return result

    def add_repair(self, id, phone, detail_name, detail_number):
        with self.__con:
            cur = self.__con.cursor()
            data = [id, phone, detail_name, detail_number]
            sql = 'INSERT INTO repair_works (appeal_number, id_employee, detail_name, detail_number) VALUES(%s, %s, %s, %s)'
            cur.execute(sql, data)

    def get_appeal_period(self, client_id):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT c.* FROM cars c WHERE id_owner = %s', (client_id, ))
            car = cur.fetchall()
            result = 0
            if car:
                for i in range(len(car)):
                    car_number = car[i]['car_number']
                    cur.execute('SELECT a.* FROM appeals a WHERE car_number = %s', (car_number, ))
                    result += cur.rowcount
                return result
            else:
                return 0

    def get_repair_period(self, id):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT r.* FROM repair_works r WHERE id_employee = %s', (id, ))
            result = cur.rowcount
            if result:
                return result
            else:
                return 0

    def get_all_repair_works(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute('SELECT r.* FROM repair_works r')
            result = cur.fetchall()
            return result