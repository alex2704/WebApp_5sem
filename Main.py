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

if __name__ == "__main__":
    app.run()

