# learning-flask

This repo is about learning-flask. I am creating a Flask App from scratch.

## See it in action
```
$ cd learning-flask
$ source venv/bin/activate
$ export FLASK_ENV=development
$ flask run
```
Then access the page in http://localhost:5000

## Listen at specific address
Set application to listen at specific address by modifying the app.run() call:

app.run(host=X.Y.W.Z)
```
$ cd learning-flask
$ source venv/bin/activate
$ export FLASK_ENV=development
$ python app.py

```
Then access the page in http://X.Y.W.Z:5000
