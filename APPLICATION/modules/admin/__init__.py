import os
import pathlib

import flask_login
from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required
from flask_security import current_user
from werkzeug.utils import redirect
from sqlalchemy.exc import OperationalError
from APPLICATION.model import User, db, Role, RolesUsers
from flask_security import utils, SQLAlchemyUserDatastore, roles_required

VERSION = 1
ENDPOINT = '/admin'
NAME = 'admin'
admin = Blueprint(NAME, __name__, template_folder='templates', static_folder='static')
MODULE = admin
MENU_ENTRY = {
    'type': 'admin',
    'label': 'Admin - Dashboard',
    'icon': 'cog',
    'endpoint': f"{ENDPOINT}/",
    'order': 100
}


@admin.record
def record_params(setup_state):
    app = setup_state.app
    admin.config = dict([(key, value) for (key, value) in app.config.items()])
    admin.logger = app.logger
    admin.app = app.config


@admin.route('/')
@roles_required('admin')
@login_required
def index():
    users = User.query.all()
    return render_template('ad_index.html', users=users)


@admin.route('/create_user')
@roles_required('admin')
@login_required
def create_user():
    return render_template('ad_create_user.html')


@admin.route('/add_user', methods=['POST'])
@roles_required('admin')
@login_required
def add_user():
    user = User.query.order_by(User.id.desc()).first()
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    if request.method == 'POST':
        if 'email' in request.form:
            email = request.form.get('email')
        if 'password' in request.form:
            password = request.form.get('password')
        if 'name' in request.form:
            name = request.form.get('name')
        if 'firstname' in request.form:
            firstname = request.form.get('firstname')
        if 'phone' in request.form:
            phone = request.form.get('phone')
        if 'signing' in request.files:
            filename = str(user.id + 1) + '.jpg'
            signing = request.files.get('signing')
            path = f"APPLICATION/{admin.app['MODULES_FOLDER']}/{'admin'}/{'signing'}"
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            try:
                signing.save(os.path.join(path, filename))
            except PermissionError:
                admin.log.error("Permission Error to create / save file to uploads folder")

        exists = db.session.query(db.exists().where(User.email == email)).scalar()
        if exists:
            flash("Utilisateur existe déja", "error")
            return redirect(url_for('admin.index'))

        encrypted_password = utils.hash_password(password)

        if not user_datastore.get_user(email):
            user_datastore.create_user(email=email, password=encrypted_password, last_name=name, first_name=firstname,
                                       phone=phone, signing=filename)

        try:
            db.session.commit()
        except OperationalError:
            admin.logger.error("Operational Error permission access database")
        user_datastore.add_role_to_user(email, 'user')  # set Role to the new User
        try:
            db.session.commit()
        except OperationalError:
            admin.logger.error("Operational Error permission access database")
    flash("Utilisateur créer", "success")
    return redirect(url_for('admin.index'))


@admin.route('/delete/<int:user_id>', methods=['POST'])
@roles_required('admin')
@login_required
def delete_user(user_id):
    user = RolesUsers.query.filter_by(user_id=user_id).first()
    if user.role_id == 1:  # role_id = 1 => Role Admin
        id = current_user.get_id()
        if int(id) == int(user_id):
            User.query.filter_by(id=user_id).delete()
            RolesUsers.query.filter_by(user_id=user_id).delete()
            try:
                db.session.commit()
            except OperationalError:
                admin.logger.error("Operational Error permission access database")
            flask_login.logout_user()
            return redirect(url_for('security.login'))
        else:  # role_id != 1 => Role User
            User.query.filter_by(id=user_id).delete()
            RolesUsers.query.filter_by(user_id=user_id).delete()
            try:
                db.session.commit()
            except OperationalError:
                admin.logger.error("Operational Error permission access database")
            return redirect(url_for('admin.index'))
    else:
        id = current_user.get_id()
        if int(id) == int(user_id):
            User.query.filter_by(id=user_id).delete()
            RolesUsers.query.filter_by(user_id=user_id).delete()
            try:
                db.session.commit()
            except OperationalError:
                admin.logger.error("Operational Error permission access database")
            flask_login.logout_user()
            return redirect(url_for('security.login'))
        else:
            User.query.filter_by(id=user_id).delete()
            RolesUsers.query.filter_by(user_id=user_id).delete()
            try:
                db.session.commit()
            except OperationalError:
                admin.logger.error("Operational Error permission access database")
            flash("Utilisateur supprimé", "success")
            return redirect(url_for('admin.index'))


@admin.route('/modify_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
@login_required
def modify_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('ad_modify_user.html', user=user)


@admin.route('/change_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
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
        if 'signing' in request.files:
            path = f"APPLICATION/{admin.app['MODULES_FOLDER']}/{'admin'}/{'signing'}"
            if user.signing:
                os.remove(os.path.join(path, user.signing))
            filename = str(user_id) + '.jpg'
            signing = request.files.get('signing')
            user.signing = filename
            try:
                signing.save(os.path.join(path, filename))
            except PermissionError:
                admin.log.error("Permission Error to create / save file to uploads folder")

        try:
            db.session.commit()
        except OperationalError:
            admin.logger.error("Operational Error permission access database")
        flash("Utilisateur modifié", "success")
    return redirect(url_for('admin.index'))
