from flask import Flask, request, g, render_template
from importlib import import_module
from os import listdir, path
from pprint import pprint
from openpyxl import Workbook
from operator import itemgetter
from time import time
from flask_mail import Mail

from flask_login import login_required
from flask_security import SQLAlchemyUserDatastore, utils, Security, user_registered


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    mail = Mail(app)
    wb = Workbook()

    # Setup Flask-Security
    from APPLICATION.model import db, User, Role #, Client, ClientMeta, InterviewMetaDef

    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    # set default role for new user
    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):
        default_role = user_datastore.find_role("user")
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()

    modules = []

    for module_name in listdir(path.join('APPLICATION', app.config['MODULES_FOLDER'])):
        m = import_module(f"APPLICATION.{app.config['MODULES_FOLDER']}.{module_name}")
        app.register_blueprint(m.MODULE, url_prefix=m.ENDPOINT)
        if m.MENU_ENTRY['type'] == 'level':
            m.MENU_ENTRY['endpoints'] = []
            for e in m.MENU_ENTRY['entries']:
                m.MENU_ENTRY['endpoints'].append(e['endpoint'])

        modules.append(m.MENU_ENTRY)

    modules = sorted(modules, key=itemgetter('order'))

    @app.before_first_request
    def before_first_request():
        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "user" -- unless they already exist
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='user', description='User')

        # Create Admin unless he already exists.
        encrypted_password = utils.hash_password('admin')
        if not user_datastore.get_user('admin@admin.com'):
            user_datastore.create_user(email='admin@admin.com', password=encrypted_password)

        encrypted_password = utils.hash_password('user')
        if not user_datastore.get_user('user@user.com'):
            user_datastore.create_user(email='user@user.com', password=encrypted_password)

        encrypted_password = utils.hash_password('test')
        if not user_datastore.get_user('test@test.com'):
            user_datastore.create_user(email='test@test.com', password=encrypted_password)

        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()

        # set Admin Role
        user_datastore.add_role_to_user('admin@admin.com', 'admin')
        user_datastore.add_role_to_user('user@user.com', 'user')
        user_datastore.add_role_to_user('test@test.com', 'user')
        db.session.commit()

    @app.before_request
    def before_request():
        g.version = app.config['VERSION']
        g.host = f"{app.config['HOST']}:{app.config['PORT']}"
        g.api = app.config['API']

        if 'static' not in request.path:
            g.time = time()
            g.endpoint = request.path
            g.modules = modules
            g.config = app.config
            #  to delete
            import random
            g.random = random.randint(0, 19999999)

            from APPLICATION.utils import get_module_from_endpoint
            g.page_title = get_module_from_endpoint(modules, request.path)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def access_denied(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
