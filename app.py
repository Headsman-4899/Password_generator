import random

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(100))
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, site, login, password):
        self.site = site
        self.login = login
        self.password = password


def generate_password():
    symbols = 'abcdefghijklmnopqrstuvwxyz'
    upper_symbols = symbols.upper()
    chars = list()
    chars.extend(symbols)
    chars.extend(upper_symbols)
    chars.extend('-()[]!@#$')
    chars.extend('0123456789')

    generated_password = ''
    random_length = random.randint(8, 15)
    for i in range(random_length):
        generated_password += random.choice(chars)

    return generated_password


@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", passwords=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        site = request.form['site']
        login = request.form['login']
        password = generate_password()

        my_data = Data(site, login, password)
        db.session.add(my_data)
        db.session.commit()

        flash("Password Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.site = request.form['site']
        my_data.login = request.form['login']
        my_data.password = generate_password()

        db.session.commit()
        flash("Password Updated Successfully")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Password Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
