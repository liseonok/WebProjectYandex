from flask import Flask
from flask_login import LoginManager

from data import db_session
from data.user import User
from blueprints.auth import auth_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, int(user_id))


def main():
    db_session.global_init("db/blogs.sqlite")

    app.register_blueprint(auth_blueprint)

    app.run(port=8888, host='localhost')


if __name__ == '__main__':
    main()