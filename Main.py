from flask import Flask, render_template, redirect, request, url_for
from DB import DB
from CheckHelper import CheckHelper
app = Flask(__name__)
app.config['DEBUG'] = True

db = DB()


@app.route('/')
@app.route('/index')
def show_clients():
    clients = db.get_clients()
    return render_template('index.html', data=clients, len=len(clients))


# отобразитб машины у данного клиента
@app.route('/client/<id>')
def show_client(id):
    data = db.show_cars(id)
    return render_template('cars.html', id=id, data=data, len=len(data), )


@app.route('/delete_car/<id>', methods=['POST'])
def del_car(id):
    id_owner = request.form['indexDeleted']
    db.delete_car(id)
    return redirect(url_for('show_client', id=id_owner))


@app.route('/add_car/<id>', methods=['POST'])
def add_car(id):
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


# удалить клиента
@app.route('/', methods=['POST'])
@app.route('/index', methods=['POST'])
def delete_client():
    if request.form['deleteClient'] == "Удалить":
        cur_stud = request.form['indexDeleted']
        db.delete_client(cur_stud)
        return redirect('/index')


@app.route('/addClient')
def show_form_add_client():
    return render_template('addClient.html')


@app.route('/addClient', methods=['POST'])
def add_client():
    # try:
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
    # except Exception as e:
    #     return "Произошла ошибка"


@app.route('/employees')
def show_employees():
    employees = db.get_employees()
    positions = db.get_all_positions()
    return render_template('employees.html', data=employees, len=len(employees), type_positions=positions,
                           lenp=len(positions))


@app.route('/employees', methods=['POST'])
def delete_employee():
    if request.form['deleteEmployee'] == "Удалить":
        cur_empl = request.form['indexDeleted']
        db.delete_employee(cur_empl)
        return redirect('/employees')


@app.route('/add_employee', methods=['POST'])
def add_employee():
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

if __name__ == "__main__":
    app.run()

