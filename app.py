from flask import Flask, render_template, url_for
from flask import redirect, flash, request
from sqlalchemy import create_engine, text
from flask_login import LoginManager, current_user, UserMixin
from forms import RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

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
        return users[id]
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Conta criada {form.username.data}!', 'success')
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