# CinemaBooking (CINEVERSE)
Online Cinema Booking web application using Flask framework
'Cineverse' :)

## Development environment
### virtual environment used && activating the venv
python3 -m venv venv
source venv/bin/activate

## Installing Flask, SQLAlchemy and setting the requiements
pip install Flask
pip install flask_sqlalchemy (using SQLAlchemy for database)
pip freeze > requirements.txt

### Installing all the packages for this project
pip install -r requirements.txt

### Database creation 
#### application context (from the terminal)
app.app_context().push()
then
db.create_all()
