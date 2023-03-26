from flask import render_template, request, flash, redirect
from database import app, db, User

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
         
        if (firstname == '' or lastname == '' or email == '' or password == '' or confirmPassword == '' ):
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
    return "Homepage"


if __name__ == "__main__":
    app.run(debug=True)
