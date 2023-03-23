from app import app
from flask_sqlalchemy import SQLAlchemy

# database creation and connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cineverse_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
