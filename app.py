from flask import Flask, render_template, url_for
from flask import redirect, flash, request
from sqlalchemy import create_engine, text
from flask_login import LoginManager, current_user, UserMixin
from flask_wtf import FlaskForm
from forms import RegistrationForm
from json2html import *

import bcrypt
import requests
import os
import json
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


KEA_URL = 'http://200.19.145.141:8000/kea'


login_manager = LoginManager(app)
engine = create_engine("sqlite+pysqlite:///database.db", echo=True, future=True)



class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn

@app.route('/')
def home():
    #if not current_user or current_user.is_anonymous:
    #    return redirect(url_for('login'))
    
    return render_template('index.html')





@app.route('/tester')
def tester():
    return {"jsonkey": "This is json value"}

@app.route('/config-get', methods=['GET','POST'])
def config_get():
    data = { "command": "config-get", "service": ["dhcp4"] }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(KEA_URL, data=json.dumps(data), headers=headers)
    result = response.json()
    print("result: ", result)
    
    # Pass json from Flask to Javascript
    return render_template('config-get.html', title='Kea config-get', data=result)
    
    
    # Convert json to html
    #input = json.dumps(response.json(), indent=4)
    #return json2html.convert(json = input, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")

@app.route('/subnet4-list')
def subnet4_list():
    f = open("subnets4.json.bkp", "r")
    content = f.read()
    content = re.sub('(//).*', '', content)
    #content = re.sub('^$\n', '', content)
    #print(content)
    #for line in range(len(content)):
    #    if line.s
    result = eval('{' + content + '}')
    return render_template('subnet4-list.html', title='Kea subnet4-list', data=result)

@app.route('/lease4-get-all', methods=['GET','POST'])
def lease4_get_all():
    data = { "command": "lease4-get-all", "service": ["dhcp4"] }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(KEA_URL, data=json.dumps(data), headers=headers)
    result = response.json()
    print("result: ", json.dumps(result, indent=2))
    
    # Pass json from Flask to Javascript
    return render_template('lease4-get-all.html', title='Kea lease4-get-all', data=result)

@app.route('/lease4-add', methods=['GET','POST'])
def lease4_add():
    if request.method == 'POST':
        ipaddress = request.form['ip-address']
        hwaddress = request.form['hw-address']
        if not ipaddress:
            flash('É necessário digitar um IP!','danger')
        elif not hwaddress:
            flash('É necessário digitar um MAC!','warning')
        else:        
            result = {'ip-address': ipaddress, 'hw-address': hwaddress}
        
    result = {}
    return render_template('lease4-add.html', title='Kea lease4-add', data=result)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if not name:
            flash('É necessário digitar um nome!','danger')
        elif not password:
            flash('É necessário digitar uma senha!','warning')
        else:
            with engine.connect() as conn:
                conn.execute(text("INSERT INTO USER (username, password) VALUES (:username, :password)"),
                [{"username": name,"password": password}],
                )
                conn.commit()
            
                result = conn.execute(text("SELECT * FROM USER"))
                print(name + password)        
                return 'Nome: '+name+' e Senha: '+password+' adicionados.'

    return render_template('login.html')    




@login_manager.user_loader
def load_user(id):
    if id in users:
        return None
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form.validate())
    print(form.is_submitted())
    print(form.validate_on_submit())
    print(form.errors)

    if form.validate_on_submit():
        password = form.email.data
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO USER (username, password) VALUES (:username, :password)"),
                [{"username": form.username.data,"password": hash}],
            )
            conn.commit()
        flash(f'Conta criada {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create')
def create():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS USER (username VARCHAR(10), password VARCHAR(10))"))
        conn.execute(
            text("INSERT INTO USER (username, password) VALUES (:username, :password)"),
            [{"username": "joao","password": "pass1"}],
        )
        conn.commit()
        result = conn.execute(text("SELECT * FROM sqlite_master"))
        return str(result.all())
        
@app.route('/select')
def select():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM USER"))
        return str(result.all())
    
@app.route('/users')
def users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM USER"))
        return render_template('users.html', title='Users', users=result)
    

if __name__ == '__main__':
    app.run(host='200.19.145.141')