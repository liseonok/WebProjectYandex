from flask import Blueprint, render_template
from data import db_session
from data.places import Place

main_blueprint = Blueprint('main', __name__, template_folder='../templates')


@main_blueprint.route('/')
def index():
    db_sess = db_session.create_session()
    places = db_sess.query(Place).filter(Place.is_private != True).all()

    return render_template('index.html', title='City Oddities', places=places)

