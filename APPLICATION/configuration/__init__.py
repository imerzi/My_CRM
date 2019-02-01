class Configuration(object):
    VERSION = '1.0.0'
    DEBUG = True
    STATUS = 'UNKNOWN'

    SECRET_KEY = '1qz3d1q6z81gr38h1y3k813hi8lq16z8d1fb024265f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = '0.0.0.0'
    PORT = 5000

    MODULES_FOLDER = 'modules'
    UPLOAD_FOLDER = 'APPLICATION/uploads/'

    # Flask Security config
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_CONFIRM_URL = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_PASSWORD_SALT = 'abcdefghijklmnopqrstuvwxyz'

    SITE_TITLE = 'PlugMusic'
    SITE_ICON = '/static/dist/img/music-solid.svg'

    # API key Google Geoloc
    API = "AIzaSyDFEEEgxAmKiT3ytDn8RWuWuafu-ylDlik"

    # Flask Mail
    # MAIL_SERVER = 'ssl0.ovh.net'
    # MAIL_PORT = 587
    # MAIL_USERNAME = 'privacy@grhconsultants.fr'
    # MAIL_PASSWORD = 'sFa8xrbxCS2aSZBozdjr'
    # MAIL_USE_TLS = True
    # MAIL_DEFAULT_SENDER = 'contact@grhservices.fr'


class Development(Configuration):
    STATUS = 'DEVELOPMENT'
