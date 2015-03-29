from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.autodoc import Autodoc
from flask.ext.babel import Babel
from config import config 

cfg = config
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()
auto = Autodoc()
babel = Babel()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(cfg[config_name])

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production
        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)
    auto.init_app(app)
    babel.init_app(app)

    from .products import products as products_blueprint
    app.register_blueprint(products_blueprint, url_prefix='/app')
    app.register_blueprint(products_blueprint, url_prefix='/')

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/app/users')

    from .stations import stations as stations_blueprint
    app.register_blueprint(stations_blueprint, url_prefix='/app/stations')

    from .operation_types import operation_types as operation_types_blueprint
    app.register_blueprint(operation_types_blueprint, url_prefix='/app/operation_types')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/app/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .api_1_0 import webapi as webapi_blueprint
    app.register_blueprint(webapi_blueprint, url_prefix='/webapi/1.0')

    return app
