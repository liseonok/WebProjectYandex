from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired


class PlaceForm(FlaskForm):
    name = StringField('Название места', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    latitude = FloatField('Широта', validators=[DataRequired()])
    longitude = FloatField('Долгота', validators=[DataRequired()])
    image = FileField('Фотография')
    is_private = BooleanField('Сделать место приватным')
    submit = SubmitField('Добавить место')
