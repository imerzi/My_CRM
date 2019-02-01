from flask import Blueprint, render_template, url_for, request, flash
from flask_login import current_user, login_required
from sqlalchemy.exc import OperationalError
from flask_security import utils

from APPLICATION.model import db, User

VERSION = 1
ENDPOINT = '/account'
NAME = 'account'
ac = Blueprint(NAME, __name__, template_folder='templates', static_folder='static')
MODULE = ac
MENU_ENTRY = {
    'type': 'entry',
    'label': 'Profil',
    'order': 5,
    'endpoint': f"{ENDPOINT}/",
    'icon': 'user',
}


@ac.record
def record_params(setup_state):
    app = setup_state.app
    ac.config = dict([(key, value) for (key, value) in app.config.items()])
    ac.app = app.config
    ac.log = app.logger


@ac.route('/')
@login_required
def index():
    user_id = current_user.get_id()
    user = User.query.filter_by(id=user_id).first()
    return render_template('ac_index.html', user=user)


@ac.route('/change_user/<int:user_id>', methods=['POST'])
@login_required
def change_user(user_id):
    if request.method == 'POST':
        user = User.query.filter_by(id=user_id).first()
        if 'email' in request.form:
            email = request.form.get('email')
            user.email = email
        if 'password' in request.form:
            password = request.form.get('password')
            if password:
                encrypted_password = utils.hash_password(password)
                user.password = encrypted_password
        if 'name' in request.form:
            name = request.form.get('name')
            user.last_name = name
        if 'firstname' in request.form:
            firstname = request.form.get('firstname')
            user.first_name = firstname
        if 'phone' in request.form:
            phone = request.form.get('phone')
            user.phone = phone

        try:
            db.session.commit()
        except OperationalError:
            ac.logger.error("Operational Error permission access database")
        flash("Utilisateur modifié", "success")
    return render_template('ac_index.html', user=user)
