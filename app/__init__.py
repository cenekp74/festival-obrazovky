from flask import Flask

app = Flask(__name__)
app.secret_key = 'dev'
app.config.from_pyfile('../instance/config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['DB_SERVER'] = 'http://localhost:5000'

from app import routs