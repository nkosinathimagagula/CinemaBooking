from base64 import b64encode
from re import sub
from database import db

def decode_image(movie):
    return b64encode(movie.image).decode('ascii')

def remove_special_chars(chars):
    special_char_regex = r'[^a-zA-Z0-9\s]+'

    return sub(special_char_regex, '', chars)

def create_seats(movie_added):
    # Dynamically creating a class for cinema room seats for each movie added
    # !!! [ for some reason I got indentation error, thus the weird format in this string below ]
    class_name = 'Seats' + str(movie_added.cinema_room) + str(movie_added.movie_id)
    class_body = """id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
c1 = db.Column(db.Integer, nullable=False)
c2 = db.Column(db.Integer, nullable=False)
c3 = db.Column(db.Integer, nullable=False)
c4 = db.Column(db.Integer, nullable=False)
c5 = db.Column(db.Integer, nullable=False)
c6 = db.Column(db.Integer, nullable=False)
c7 = db.Column(db.Integer, nullable=False)
c8 = db.Column(db.Integer, nullable=False)

def __init__(self, c1, c2, c3, c4, c5, c6, c7, c8):
    self.c1 = c1
    self.c2 = c2
    self.c3 = c3
    self.c4 = c4
    self.c5 = c5
    self.c6 = c6
    self.c7 = c7
    self.c8 = c8"""
    class_dictionary = {}
    exec(class_body, globals(), class_dictionary)
        
    locals()['Seats' + str(movie_added.cinema_room) + str(movie_added.movie_id)] = type(class_name, (db.Model,), class_dictionary)

    db.create_all()


    # add 4 rows for seats
    for _ in range(4):
        row = locals()['Seats' + str(movie_added.cinema_room) + str(movie_added.movie_id)](0, 0, 0, 0, 0, 0, 0, 0)
        db.session.add(row)
        db.session.commit()
