from APPLICATION import create_app
from APPLICATION.configuration import Development
from logging.handlers import RotatingFileHandler
import logging


app = create_app(Development)

formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler('exception.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

if app.config['STATUS'] == 'PRODUCTION':
    context = ('cert/cert.pem', 'cert/key.pem')
    app.run(host=app.config['HOST'], port=app.config['PORT'], ssl_context=context)
else:
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
