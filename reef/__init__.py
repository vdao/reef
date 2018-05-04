import os
import logging

from logging import FileHandler

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, upgrade

from config import Config

bootstrap = Bootstrap()
database = SQLAlchemy()

import reef.model

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if not app.debug:
        file_handler = FileHandler(app.config['LOG_FILE'])
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

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

    from . import blog
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        database.session.rollback()
        return render_template('500.html'), 500

    return app