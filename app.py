from flask import render_template, flash, redirect, request
from database import app, db, User, Movie
from utils import decode_image, remove_special_chars
from datetime import datetime


# Admin routes ------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/admin/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['movie_name']
        category = request.form['category']
        image = request.files['image']
        description = request.form['description']
        date_time = datetime.strptime(request.form['date_time'], '%Y-%m-%dT%H:%M')
        price = request.form['price']
        cinema_room = request.form['cinema_room']

        movie = Movie(name, category, image.read(), description, date_time, price, cinema_room)

        db.session.add(movie)
        db.session.commit()

        movie_added = Movie.query.filter_by(name=name).first()

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
        globals()['Seats' + str(movie_added.cinema_room) + str(movie_added.movie_id)] = type(class_name, (db.Model,),
                                                                                             class_dictionary)

        db.create_all()

        # add 4 rows for seats
        for _ in range(4):
            row = globals()['Seats' + str(movie_added.cinema_room) + str(movie_added.movie_id)](0, 0, 0, 0, 0, 0, 0, 0)
            db.session.add(row)
            db.session.commit()

    movies = Movie.query.all()
    images = map(decode_image, movies)

    return render_template('admin/add.html', images=list(images))


# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# User routes -------------------------------------------------------------------------------------------------------------------------------------------------
# landing page
@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if firstname == '' or lastname == '' or email == '' or password == '' or confirmPassword == '':
            flash('Please fill in all the blanks!', 'error')
        elif password == confirmPassword:

            # might have to change this since it handles any error by flashing this message 
            # might want to try this
            #
            # user = User.query.filter_by(email=email).first()
            # if user == None
            #   add user to the table
            # else
            #   flash the message
            #
            # then except will come after this ...

            try:
                user = User(firstname, lastname, email, password)

                db.session.add(user)
                db.session.commit()

                flash('Successfully signed up! You can now login.', 'message')
                return redirect('/login')
            except:
                flash('Email already exist. Please try to login!', 'error')
        else:
            flash('passwords don\'t match!', 'error')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            flash('Please fill in all the blanks!', 'error')
        else:
            try:
                user = User.query.filter_by(email=email).first()

                if user != None:
                    if user.password == password:
                        return redirect('/home/')
                    else:
                        flash('Wrong password. Please try again!', 'error')
                else:
                    flash('User does not exist. Please signup first!', 'error')
            except:
                return "ERROR QUERYING THE DATABASE!"

    return render_template('login.html')


@app.route('/home/')
def home():
    categories = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'History',
                  'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller']
    movies = {}

    for category in categories:
        locals()[category.lower()] = Movie.query.filter_by(category=category).all()
        locals()[category.lower() + '_images'] = list(map(decode_image, locals()[category.lower()]))

        # key       :   value
        # category  :   [ movies with details , decoded images for that category ]
        movies[category] = [locals()[category.lower()], locals()[category.lower() + '_images']]


    return render_template('home.html', movies=movies, zip=zip, datetime=datetime, format_str=remove_special_chars)


@app.route('/home/movie/<string:movie_name>-<int:movie_id>/details')
def details(movie_name, movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    image = decode_image(movie)
    return render_template('details.html', movie=movie, image=image, datetime=datetime);


if __name__ == "__main__":
    app.run(debug=True)
