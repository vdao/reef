import os

from flask import Flask
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

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping(
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        )
        app.config.from_object(Config)
        app.config.from_pyfile('deploy-config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap.init_app(app)
    database.init_app(app)
    migration = Migrate(app, database)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')

    return app
