from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config.from_object(Config)
db = SQLAlchemy(app)
