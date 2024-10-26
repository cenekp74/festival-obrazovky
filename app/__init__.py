from flask import Flask

app = Flask(__name__)
app.secret_key = 'dev'

app.config['DB_SERVER'] = 'https://jsnsgekom.cz'
app.config["CURRENT_DAY"] = 1
app.config.from_pyfile('../instance/config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

from app import routs