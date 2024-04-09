from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length


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
    image = FileField('Изображение', validators=[
        FileRequired('Прикрепите изображение!'),
        FileAllowed(['jpg', 'jpeg', 'png'], message='Неверный формат файла!')])
    submit = SubmitField('Добавить фильм')