import os

import logging
from logging.config import dictConfig

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config

bootstrap = Bootstrap()
database = SQLAlchemy()

import reef.model

from flask.logging import default_handler

from logging import FileHandler, StreamHandler, Formatter

formatter = Formatter('[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d %(message)s')

file_handler = FileHandler('application.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

default_handler.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(default_handler)
root.addHandler(file_handler)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.logger.info('Starting application at %s' % os.getcwd())

    app.logger.info('Trying to load properties from config.py')
    app.config.from_object(Config)
    if test_config is None:
        app.logger.info('Trying to load properties from deploy-config.py')
        app.config.from_pyfile('deploy-config.py', silent=True)
    else:
        app.logger.info('Trying to load the test config')
        app.config.from_mapping(test_config)

    app.logger.info('Ensure the instance folder exists')
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap.init_app(app)
    database.init_app(app)
    migration = Migrate(app, database)

    app.logger.info('Loading blueprints')
    from . import auth
    app.register_blueprint(auth.bp)

    from . import books
    app.register_blueprint(books.bp)

    from . import readers
    app.register_blueprint(readers.bp)

    from . import catalog
    app.register_blueprint(catalog.bp)

    from . import calendar
    app.register_blueprint(calendar.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    from . import statistics
    app.register_blueprint(statistics.bp)

    app.add_url_rule('/', endpoint='catalog.index')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        database.session.rollback()
        return render_template('500.html'), 500

    admin = Admin(app, name='reef-admin', template_mode='bootstrap3')
    admin.add_view(ModelView(reef.model.Reader, database.session))
    admin.add_view(ModelView(reef.model.User, database.session))
    admin.add_view(ModelView(reef.model.Post, database.session))
    admin.add_view(ModelView(reef.model.Book, database.session))
    admin.add_view(ModelView(reef.model.BookRecord, database.session))
    admin.add_view(ModelView(reef.model.Category, database.session))

    return app
