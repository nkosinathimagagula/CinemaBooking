from flask import render_template, Blueprint, request
from database import db, Movie
from datetime import datetime
from utils import decode_image, create_seats

admin_page = Blueprint('admin_page',__name__, template_folder='templates')

@admin_page.route('/admin/upload/', methods=['GET', 'POST'])
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

        create_seats(movie_added)


    movies = Movie.query.all()
    images = map(decode_image, movies)

    return render_template('admin/add.html', images=list(images))
