

from flask import Flask, render_template, render_template_string, url_for
from flask_login import LoginManager, current_user, UserMixin
from flask import render_template_string,  redirect
from sqlalchemy import create_engine, text

app = Flask(__name__)

login_manager = LoginManager(app)
engine = create_engine("sqlite+pysqlite:///database.db", echo=True, future=True)

users = {}

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


@app.route('/login')
def login():
    return render_template('login.html')



@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None


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