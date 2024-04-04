from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db2.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRET'

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    reviews = db.relationship('Review', back_populates='movie')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    movie = db.relationship('Movie', back_populates='reviews')


class ReviewForm(FlaskForm):
    name = StringField('Ваше имя', validators=[
        DataRequired(message='Поле не должно быть пустым'),
        Length(max=255, message='Введите имя до 255 символов')
    ])
    text = TextAreaField('Текст отзыва', validators=[
        DataRequired(message='Поле не должно быть пустым')])
    score = SelectField('Оценка', coerce=int, choices=[
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
        (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')
    ])
    submit = SubmitField('Добавить отзыв')


class MovieForm(FlaskForm):
    title = StringField('Название', validators=[
        DataRequired(message='Поле не должно быть пустым'),
        Length(max=255, message='Введите название до 255 символов')
    ])
    description = TextAreaField('Описание', validators=[
        DataRequired(message='Поле не должно быть пустым')])
    image = FileField('Изображение', validators=[FileRequired('Прикрепите изображение!')])
    submit = SubmitField('Добавить фильм')


db.create_all()


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           movies=movies)


@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        average_score = round(sum(review.score for review in movie.reviews) / len(movie.reviews), 2)
    else:
        average_score = 0
    form = ReviewForm(score=10)
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('movie.html',
                           movie=movie,
                           avg_score=average_score,
                           form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data
        # movie.image = form.image.data -- решить вопрос с путями к файлам(сохранять на сервер)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_movie.html',
                           form=form)


@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.created_date.desc()).all()
    return render_template('reviews.html',
                           reviews=reviews)


@app.route('/delete_review/<int:id>')
def delete_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews'))


if __name__ == '__main__':
    app.run()
