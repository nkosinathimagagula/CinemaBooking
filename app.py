from flask import render_template, flash, redirect, request, session
from admin import admin_page
from database import app, db, User, Movie, Ticket
from sqlalchemy import text
from datetime import datetime
from utils import decode_image, remove_special_chars, createTicketNumber, formatRow, formatColumn


# Register admin routes ---------------------------------------------------------------------------------------------------------------------------------------
app.register_blueprint(admin_page)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------

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


    return render_template('home.html', movies=movies, zip=zip, datetime=datetime, len=len, format_str=remove_special_chars)


@app.route('/home/movie/<string:movie_name>-<int:movie_id>/details')
def details(movie_name, movie_id):
    movie = Movie.query.filter_by(movie_id=movie_id).first()
    image = decode_image(movie)
    return render_template('details.html', movie=movie, image=image, datetime=datetime, format_str=remove_special_chars);


@app.route('/home/movie/<string:movie_name>-<int:movie_id>/booking/seat-selection-<string:cinema_room>/', methods=['GET', 'POST'])
def seat_selection(movie_name, movie_id, cinema_room):
    
    movie = Movie.query.filter_by(movie_id=movie_id).first()

    with db.engine.connect() as connection:
        results = connection.execute(text('SELECT * FROM seats' + str(cinema_room) + str(movie_id)))
    
    seats = []
    # remove ids
    for tuple in results:
        temp = []
        for index in range(len(tuple) - 1):
            temp.append(tuple[index + 1])
        seats.append(temp)
        

    if request.method == 'POST':
        seats_selected = request.form['seats_selected']
        
        if seats_selected != '':
            session['seats_selected'] = seats_selected
            return redirect('/home/movie/' + movie_name + '-' + str(movie_id) + '/booking/seat-selection-' + cinema_room + '/checkout/')
    
    return render_template('seat_selection.html', movie=movie, seats=seats, enumerate=enumerate)


@app.route('/home/movie/<string:movie_name>-<int:movie_id>/booking/seat-selection-<string:cinema_room>/checkout/', methods=['GET', 'POST'])
def checkout(movie_name, movie_id, cinema_room):
    seats_selected = session['seats_selected'].split(',')
    movie = Movie.query.filter_by(movie_id=movie_id).first()

    details = {}

    if request.method == 'POST':
        # work on this card info later ------------------------------- !!!
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']

        name_on_card = request.form['name_on_card']
        card_number = request.form['card_number']
        exp_date = request.form['exp_date']
        cvv = request.form['cvv']
        # ------------------------------------------------------------ !!!


        for index, seat in enumerate(seats_selected):
            names = request.form['c_' + str(index)]

            details[seat] = names

            # CRUD operations on the database

            # change seat number to 2D array indexing
            seat_index = [formatRow(seat[0]), formatColumn(seat[1])]
            
            # write to the seats table
            with db.engine.connect() as connection:
                print(str(cinema_room), str(movie_id), seat_index[1], seat_index[0])
                connection.execute(text('UPDATE seats' + str(cinema_room) + str(movie_id) + ' SET ' + seat_index[1] + ' = 1 WHERE id = ' + str(seat_index[0])))
                connection.commit()

            # Create a ticket and add it to the database
            ticket = Ticket(createTicketNumber(movie_name), names.split(' ')[0], names.split(' ')[1], movie.name, cinema_room, seat)

            movie.available_seats = movie.available_seats - 1
            movie.sold_seats = movie.sold_seats + 1

            db.session.add(ticket)
            db.session.commit()

            return 'BOOKED SUCCESSFULLY!'
    
    return render_template('checkout.html', seats_selected=seats_selected, movie=movie, len=len, datetime=datetime, enumerate=enumerate)


if __name__ == "__main__":
    app.run(debug=True)
