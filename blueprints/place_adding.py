import os

from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from data import db_session
from data.places import Place
from forms.PlaceForm import PlaceForm


place_blueprint = Blueprint('place', __name__, template_folder='../templates')


@place_blueprint.route('/adding', methods=['GET', 'POST'])
@login_required
def adding():
    form = PlaceForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            filename = None
            file = form.image.data

            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(current_app.static_folder, 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))

            place = Place(
                name=form.name.data,
                description=form.description.data,
                address=form.address.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                image_filename=filename,
                is_private=form.is_private.data,
                user_id=current_user.id
            )

            db_sess.add(place)
            db_sess.commit()
            return redirect(url_for('main.index'))
        finally:
            db_sess.close()

    return render_template('adding.html', title='Добавить место', form=form)