from flask import Flask, render_template, redirect, request
from DB import DB
app = Flask(__name__)
app.config['DEBUG'] = True

db = DB()


@app.route('/')
@app.route('/index')
def show_clients():
    clients = db.get_clients()
    return render_template('index.html', data=clients, len=len(clients))


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


if __name__ == "__main__":
    app.run()

