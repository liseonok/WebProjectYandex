from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_again = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают')]
    )
    submit = SubmitField('Зарегистрироваться')