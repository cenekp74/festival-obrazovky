from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'dev'

app.config['DB_SERVER'] = 'https://jsnsgekom.cz'
app.config["CURRENT_DAY"] = 1
app.config.from_pyfile('../instance/config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = "login"

from app import routs

with open("instance/reload.txt", "w") as f:
    f.write("0")