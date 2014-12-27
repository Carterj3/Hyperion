# https://i.stack.imgur.com/31I6E.jpg
# http://flask.pocoo.org/docs/0.10/tutorial/dbinit/#tutorial-dbinit

# pip install Flask
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# openssl genrsa -out nephthys.io.key 2048
# openssl req -new -x509 -key nephthys.io.key -out nephthys.io.cert -days 3650 -subj /CN=Nephthys.io

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'SuperDuperSecretDevKey'
USERNAME = 'admin'
PASSWORD = 'admin'

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app = Flask(__name__)
  app.config.from_object(__name__)
  app.run()