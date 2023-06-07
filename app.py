from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask!<br>Hehehehe'

@app.route('/login')
def login():
    return 'Please! Log in!'
    