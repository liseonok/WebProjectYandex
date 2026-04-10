from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

from data import db_session
from data.user import User
from forms.LoginForm import LoginForm, RegisterForm


auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates'
)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))

        return render_template(
            'login.html',
            title='Вход в аккаунт',
            form=form,
            message='Неправильная почта или пароль'
        )

    return render_template(
        'login.html',
        title='Вход в аккаунт',
        form=form
    )


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        existing_user = db_sess.query(User).filter(User.email == form.email.data).first()
        if existing_user:
            return render_template(
                'register.html',
                title='Регистрация',
                form=form,
                message='Пользователь с такой почтой уже существует'
            )

        user = User(
            username=form.name.data,
            email=form.email.data,
            password=form.password.data
        )

        db_sess.add(user)
        db_sess.commit()

        return redirect(url_for('auth.login'))

    return render_template(
        'register.html',
        title='Регистрация',
        form=form
    )


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))