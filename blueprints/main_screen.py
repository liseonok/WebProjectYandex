from flask import Blueprint, render_template, request
from data import db_session
from data.places import Place

main_blueprint = Blueprint('main', __name__, template_folder='../templates')


@main_blueprint.route('/')
def index():
    db_sess = db_session.create_session()
    try:
        places = db_sess.query(Place).filter(Place.is_private != True).all()

        lon = float(request.args.get('lon', 37.617))
        lat = float(request.args.get('lat', 55.758))
        zoom = int(request.args.get('zoom', 10))
        points = []
        for place in places:
            points.append(f"{place.longitude},{place.latitude},pmvvl{place.id}")

        pt = "~".join(points)
        print(f'{pt} string')

        map_url = (
            f"https://static-maps.yandex.ru/v1?"
            f"ll={lon},{lat}&z={zoom}&size=650,450&lang=ru_RU"
            f"&pt={pt}&apikey=79d631f0-9469-4ff4-835b-4498b7ffe6de"
        )


        return render_template(
            'index.html',
            title='Urban Oddities',
            map_url=map_url,
            lon=lon,
            lat=lat,
            zoom=zoom,
            places=places
        )
    finally:
        db_sess.close()


@main_blueprint.route('/places/<place_id>')
def learn_more(place_id):
    print(f'{place_id} string')
    db_sess = db_session.create_session()
    try:
        place = db_sess.query(Place).get(place_id)
        print(f'{place} string')
        return render_template('place.html', title=place.name, place=place)
    finally:
        db_sess.close()

