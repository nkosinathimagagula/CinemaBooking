from app import app
from flask_sqlalchemy import SQLAlchemy

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
