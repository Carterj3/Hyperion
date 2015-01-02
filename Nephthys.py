# https://i.stack.imgur.com/31I6E.jpg
# http://flask.pocoo.org/docs/0.10/tutorial/dbinit/#tutorial-dbinit

# pip install Flask
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# pip install pyopenssl
# openssl genrsa -out lesuorac.com.key 2048
# openssl req -new -x509 -key lesuorac.com.key -out lesuorac.com.cert -days 365 -subj /CN=lesuorac.com

# configuration
class config(object):
  DATABASE = 'flaskr.db'
  DEBUG = True
  SECRET_KEY = 'SuperDuperSecretDevKey'
  USERNAME = 'admin'
  PASSWORD = 'admin'
  SERVER_NAME = 'localhost:8081'

app = Flask(__name__)
app.config.from_object(config)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

##https://stackoverflow.com/questions/7512698/flask-subdomain-routing
@app.route("/", subdomain="nephthys")
def eggs_hello():
  return "Hello Eggs!"

@app.route("/")
def hello():
  return "You forgot a subdomain."
  
class Nephthys:
  pass

if __name__ == "__main__":
  app.run(host='localhost',port=8081, debug = True)
  # app.run(host='127.0.0.1',port=8081, debug = True, ssl_context=('dev-nephthys.io.cert', 'dev-nephthys.io.key'))