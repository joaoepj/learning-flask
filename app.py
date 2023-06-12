

from flask import Flask, url_for
from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, current_user, UserMixin
from flask import render_template_string, redirect
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.config['LDAP_HOST'] = 'odie-dev.dr.ufu.br'
app.config['LDAP_BASE_DN'] = 'dc=ufu,dc=br'
app.config['LDAP_USER_DN'] = 'ou=people'
app.config['LDAP_BIND_USER_DN'] = None
app.config['LDAP_BIND_USER_PASSWORD'] = None

login_manager = LoginManager(app)
ldap_manager = LDAP3LoginManager(app)
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
    
    template = """
    <div color=grey>Hello</div>
    <h1>Welcome: {{ current_user.data }}</h1>
    <h2>{{ current_user.dn }}</h2>
    <a href="/createtable">Criar tabela</a><br>
    <a href="/selecttable">Ler tabela</a><br>
    <a href="/login">Login</a>
    """

    return render_template_string(template)


@app.route('/login')
def login():
    template = """
    <style>
    .header {color:red;}
    .footer {background-color:lightgrey;}
    </style>
    <div class="header footer">Cabeçalho</div>
    <div>
    <h1>Seja bem vindo: {{ current_user.data }}</h1>
    <h2>abc{{ current_user.dn }}</h2>
    <a href="/createtable">Criar tabela de banco de dados</a>
    </div>
    <div class="footer">Rodapé</div>
    """

    return render_template_string(template)


@app.route('/manual_login')
def manual_login():
    app.ldap3_login_manager.authenticate('joao','R3s!l13nc3')
    return current_user

@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None


@app.route('/createtable')
def createtable():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS USER (username VARCHAR(10), password VARCHAR(10))"))
        conn.execute(
            text("INSERT INTO USER (username, password) VALUES (:username, :password)"),
            [{"username": "joao","password": "pass1"}],
        )
        conn.commit()
        result = conn.execute(text("SELECT * FROM sqlite_master"))
        return str(result.all())
        
@app.route('/selecttable')
def selecttable():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM USER"))
        return str(result.all())