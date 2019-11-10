from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from DB import DB
app = Flask(__name__)
app.config['DEBUG'] = True
Bootstrap(app)

db = DB()


@app.route('/')
@app.route('/index')
def main():
    clients = db.get_clients()
    return render_template('index.html', data=clients, len=len(clients))


if __name__ == "__main__":
    app.run()

