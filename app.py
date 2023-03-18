from flask import Flask, render_template

app = Flask(__name__)

# landing page
@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)
