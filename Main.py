from flask import Flask, render_template, redirect, request, url_for, session
from DB import DB
from CheckHelper import CheckHelper
import bcrypt
app = Flask(__name__)
app.config['DEBUG'] = True

db = DB()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_pass = bcrypt.hashpw(password, bcrypt.gensalt())
        db.add_user(name, hash_pass)
        session['name'] = name
        session['priveleges'] = db.get_priveleges(name)
        return redirect('/index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = db.login(name, password)
        if user:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['name'] = user['username']
                session['priveleges'] = db.get_priveleges(name)
                return redirect('/index')
            else:
                return "Error password or user don't match"
        else:
            return "Error password or user don't match"
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')


# отобразить всех клиентов
@app.route('/')
@app.route('/index')
def show_clients():
    clients = db.get_clients()
    return render_template('index.html', data=clients, len=len(clients))


# отобразить машины у данного клиента
@app.route('/client/<id>')
def show_client(id):
    if session:
        if session['priveleges']:
            data = db.show_cars(id)
            return render_template('cars.html', id=id, data=data, len=len(data))
    else:
        return redirect('/index')


# удалить машину у данного клиента
@app.route('/delete_car/<id>', methods=['POST'])
def del_car(id):
    if session:
        if session['priveleges']:
            id_owner = request.form['indexDeleted']
            db.delete_car(id)
            return redirect(url_for('show_client', id=id_owner))
    return redirect('/index')


# Добавить машину клиенту
@app.route('/add_car/<id>', methods=['POST'])
def add_car(id):
    if session:
        if session['priveleges']:
            if request.form['addCar'] == "Подтвердить":
                number = request.form['number']
                processed_text_number = number.upper()
                mark = request.form['mark']
                processed_text_mark = mark.upper()
                issue_date = request.form['issue_date']
                check = CheckHelper.check_true_date(issue_date)
                if check:
                    issue = CheckHelper.get_date_from_str(issue_date)
                    db.add_car(processed_text_number, id, processed_text_mark, issue)
                else:
                    return "Введенная дата не верна"
                return redirect(url_for('show_client', id=id))
    else:
        return redirect('/index')


# удалить клиента
@app.route('/', methods=['POST'])
@app.route('/index', methods=['POST'])
def delete_client():
    if session:
        if session['priveleges']:
            if request.form['deleteClient'] == "Удалить":
                cur_stud = request.form['indexDeleted']
                db.delete_client(cur_stud)
                return redirect('/index')
    else:
        return redirect('/index')


# Показать форму где можно добавить клиента
@app.route('/addClient')
def show_form_add_client():
    if session:
        if session['priveleges']:
            return render_template('addClient.html')
    else:
        return redirect('/index')


# Добавить клиента
@app.route('/addClient', methods=['POST'])
def add_client():
    if session:
        if session['priveleges']:
            if request.form['addClient'] == "Подтвердить":
                name = request.form['name']
                processed_text_name = name.upper()
                phone = request.form['phone']
                processed_text_phone = phone.upper()
                surname = request.form['surname']
                processed_text_surname = surname.upper()
                patronymic = request.form['patronymic']
                processed_text_patronymic = patronymic.upper()
                db.add_client(processed_text_name, processed_text_surname,
                              processed_text_patronymic, processed_text_phone)
                return redirect('/index')
    else:
        return redirect('/index')


# отобразить всех сотрудников
@app.route('/employees')
def show_employees():
    employees = db.get_employees()
    positions = db.get_all_positions()
    return render_template('employees.html', data=employees, len=len(employees), type_positions=positions,
                           lenp=len(positions))


# удалить сотрудника
@app.route('/employees', methods=['POST'])
def delete_employee():
    if session:
        if session['priveleges']:
            if request.form['deleteEmployee'] == "Удалить":
                cur_empl = request.form['indexDeleted']
                db.delete_employee(cur_empl)
                return redirect('/employees')
    else:
        return redirect('/index')


# добавить сотрдуника
@app.route('/add_employee', methods=['POST'])
def add_employee():
    if session:
        if session['priveleges']:
            if request.form['addEmployee'] == "Подтвердить":
                name = request.form['name']
                surname = request.form['surname']
                patronymic = request.form['patronymic']
                born_date = request.form['born_date']
                check = CheckHelper.check_true_date(born_date)
                address = request.form['address']
                phone = request.form['phone']
                id_position = request.form['position']
                work_time = request.form['work_time']
                prize = request.form['prize']
                if check:
                    birth = CheckHelper.get_date_from_str(born_date)
                    db.add_employee(name, surname, patronymic, birth, address, phone, id_position, work_time, prize)
                else:
                    return "Введенная дата не верна"
                return redirect(url_for('show_employees'))
    else:
        return redirect('/index')


# отобразить форму для изменение клиента
@app.route("/change_client/<id>")
def change_client(id):
    if session:
        if session['priveleges']:
            data = db.get_value('clients', 'id', id)
            names = list(data[0].keys())
            # db.change_value('clients', 'surname', val, 'id', id)
            return render_template('updateClient.html', data=data, len=len(data[0]), names=names)
    else:
        return redirect('/index')


# вносит изменение в клиента
@app.route("/change_client/<id>", methods=['POST'])
def set_client(id):
    if session:
        if session['priveleges']:
            if request.form['changeClient'] == "Изменить":
                param = request.form['param']
                set = request.form['set']
                db.change_value('clients', param, set, 'id', id)
            return redirect(url_for("change_client", id=id))
    else:
        return redirect('/index')


# отобразить форму для изменения авто
@app.route("/change_car/<number>")
def change_car(number):
    if session:
        if session['priveleges']:
            data = db.get_value('cars', 'car_number', number)
            names = list(data[0].keys())
            names.remove('id_owner')
            return render_template('updateCar.html', data=data, len=len(data[0]) - 1, names=names)
    else:
        redirect('/index')


# изменить авто
@app.route("/change_car/<number>", methods=['POST'])
def set_car(number):
    if session:
        if session['priveleges']:
            if request.form['changeCar'] == "Изменить":
                param = request.form['param']
                set = request.form['set']
                if param == 'issue_date':
                    check = CheckHelper.check_true_date(set)
                    if check:
                        set = CheckHelper.get_date_from_str(set)
                    else:
                        return redirect(url_for("change_car", number=number))
                db.change_value('cars', param, set, 'car_number', number)
            return redirect(url_for("change_car", number=number))
    else:
        redirect('/index')


# отобразить форму для изменения сотрудника
@app.route("/change_employee/<id>")
def change_employee(id):
    if session:
        if session['priveleges']:
            data = db.get_value('employees', 'id', id)
            names = list(data[0].keys())
            names.remove('id_position')
            return render_template('updateEmployee.html', data=data, len=len(data[0]) - 1, names=names)
    else:
        return redirect('/index')


@app.route("/change_employee/<id>", methods=['POST'])
def set_employee(id):
    if session:
        if session['priveleges']:
            if request.form['changeEmployee'] == "Изменить":
                param = request.form['param']
                set = request.form['set']
                if param == 'birth_date':
                    check = CheckHelper.check_true_date(set)
                    if check:
                        set = CheckHelper.get_date_from_str(set)
                    else:
                        return redirect(url_for("change_employee", id=id))
                db.change_value('employees', param, set, 'id', id)
            return redirect(url_for("change_employee", id=id))
    else:
        return redirect('/index')


@app.route('/positions')
def show_positions():
    data = db.show_positions()
    return render_template('positions.html', data=data, len=len(data))


@app.route('/add_position', methods=['POST'])
def add_position():
    if session:
        if session['priveleges']:
            if request.form['addPosition'] == "Подтвердить":
                position = request.form['position']
                salary = request.form['salary']
                db.add_position(position, salary)
                return redirect('/positions')
    else:
        return redirect('/index')


@app.route('/del_position/<id>', methods=['POST'])
def del_position(id):
    if session:
        if session['priveleges']:
            if request.form['deletePosition'] == "Удалить":
                cur_pos= request.form['indexDeleted']
                db.delete_position(cur_pos)
                return redirect('/positions')
    else:
        return redirect('/index')


@app.route('/change_position/<id>')
def change_position(id):
    if session:
        if session['priveleges']:
            data = db.get_value('position', 'id', id)
            names = list(data[0].keys())
            return render_template('updatePosition.html', data=data, len=len(data[0]), names=names)
    else:
        return redirect('/index')


@app.route("/change_position/<id>", methods=['POST'])
def set_position(id):
    if session:
        if session['priveleges']:
            if request.form['changePosition'] == "Изменить":
                param = request.form['param']
                set = request.form['set']
                db.change_value('position', param, set, 'id', id)
            return redirect(url_for("change_position", id=id))
    else:
        return redirect('/index')


@app.route('/appeals')
def show_appeals():
    data = db.show_appeals()
    cars = db.get_all_cars()
    return render_template('appeals.html', data=data, len=len(data), cars=cars, lencars=len(cars))


@app.route('/add_appeal', methods=['POST'])
def add_appeal():
    if request.form['addAppeal'] == "Подтвердить":
        car_number = request.form['car_number']
        fault = request.form['fault']
        db.add_appeal(car_number, fault)
        return redirect('/appeals')


@app.route('/del_appeal/<id>', methods=['POST'])
def del_appeal(id):
    if session:
        if session['priveleges']:
            if request.form['deleteAppeal'] == "Удалить":
                cur_pos = request.form['indexDeleted']
                db.delete_appeal(cur_pos)
                return redirect('/appeals')
    else:
        return redirect('/index')


@app.route('/change_appeal/<id>')
def change_appeal(id):
    if session:
        if session['priveleges']:
            data = db.get_value('appeals', 'appeal_number', id)
            cars = db.get_all_cars()
            names = list(data[0].keys())
            return render_template('updateAppeal.html', data=data, len=len(data[0]), names=names, cars=cars, lencars=len(cars))
    else:
        return redirect('/index')


@app.route("/change_appeal/<id>", methods=['POST'])
def set_appeal(id):
    if session:
        if session['priveleges']:
            if request.form['changeAppeal'] == "Изменить":
                param = request.form['param']
                set = request.form['set']
                db.change_value('appeals', param, set, 'appeal_number', id)
            return redirect(url_for("change_appeal", id=id))
    else:
        return redirect('/index')



if __name__ == "__main__":
    app.secret_key = "2704#!AlexBakulin)"
    app.run()

