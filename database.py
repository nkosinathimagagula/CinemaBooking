from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'viuyrted768cvvbyrc8674rtedct'

# database creation and connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cineverse_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TABLES
class User(db.Model):
    # COLUMNS
    user_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

class Movie(db.Model):
    # COLUMNS
    movie_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    name = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    cinema_room = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False, default=32)
    sold_seats = db.Column(db.Integer, nullable=False, default=0)


    def __init__(self, name, category, image, description, date_time, price, cinema_room):
        self.name = name
        self.category = category
        self.image = image
        self.description = description
        self.date_time = date_time
        self.price = price
        self.cinema_room = cinema_room
