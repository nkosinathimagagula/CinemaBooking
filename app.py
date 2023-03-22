from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'viuyrted768cvvbyrc8674rtedct'

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
            flash('Successfully signed up! You can now login.', 'message')
            return redirect('/login')
        else:
            flash('passwords don\'t match!', 'error')
        
       
            

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
