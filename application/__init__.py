from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['SECRET_KEY'] = 'b9a5f346-e34e-4a0b-9b2a-4e9c309c735e'

db = SQLAlchemy(app)



from application import routes
