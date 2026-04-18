import os

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from forms.ProfileEdit import ProfileForm
from data import db_session
from data.places import Place
from data.user import User
from forms.PlaceProfileEdit import EditPlaceForm

profile_blueprint = Blueprint('profile', __name__, template_folder='templates')


@profile_blueprint.route('/profile')
@login_required
def profile():
    db_sess = db_session.create_session()
    try:
        places = db_sess.query(Place).filter(Place.user_id == current_user.id).all()

        return render_template(
            'profile.html',
            title='Профиль',
            places=places
        )
    finally:
        db_sess.close()


@profile_blueprint.route('/profile_edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            user = db_sess.get(User, current_user.id)
            user.username = form.name.data
            user.email = form.email.data
            db_sess.commit()
            return redirect(url_for('profile.profile'))
        finally:
            db_sess.close()

    form.name.data = current_user.username
    form.email.data = current_user.email

    return render_template(
        'edit_profile.html',
        title='Редактировать профиль',
        form=form
    )


@profile_blueprint.route('/edit_place/<int:place_id>', methods=['GET', 'POST'])
@login_required
def edit_place(place_id):
    db_sess = db_session.create_session()
    try:
        place = db_sess.query(Place).filter(
            Place.id == place_id,
            Place.user_id == current_user.id).first()

        if not place:
            return redirect(url_for('profile.profile'))

        form = EditPlaceForm()

        if form.validate_on_submit():
            place.name = form.name.data
            place.description = form.description.data
            place.address = form.address.data
            place.latitude = form.latitude.data
            place.longitude = form.longitude.data
            place.is_private = form.is_private.data

            file = form.image.data
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(current_app.static_folder, 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                place.image_filename = filename

            db_sess.commit()
            return redirect(url_for('profile.profile'))

        if form.is_submitted() is False:
            form.name.data = place.name
            form.description.data = place.description
            form.address.data = place.address
            form.latitude.data = place.latitude
            form.longitude.data = place.longitude
            form.is_private.data = place.is_private

        return render_template(
            'edit_place.html',
            title='Редактировать место',
            form=form,
            place=place
        )
    finally:
        db_sess.close()