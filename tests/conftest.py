import os
import pytest

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reef import create_app
from reef import database

TESTDB = 'test_project.db'
TESTDB_PATH = os.path.join(os.path.dirname(__file__), TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH

ALEMBIC_CONFIG = os.path.join(os.path.dirname(__file__), '../migrations/alembic.ini')

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
        'WTF_CSRF_ENABLED' : False,
    }
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    db(request)

    return app


@pytest.fixture(scope='session')
def db(request):
    engine = create_engine(TEST_DATABASE_URI, echo=True)
    session_factory = sessionmaker(bind=engine)
    print('\n----- CREATE TEST DB CONNECTION POOL\n')

    _db = {
        'engine': engine,
        'session_factory': session_factory,
    }
    alembic_config = AlembicConfig(ALEMBIC_CONFIG)
    alembic_config.set_main_option('sqlalchemy.url', TEST_DATABASE_URI)
    alembic_upgrade(alembic_config, 'head')
    print('\n----- RUN ALEMBIC MIGRATION\n')
    yield _db
    print('\n----- CREATE TEST DB INSTANCE POOL\n')

    engine.dispose()
    print('\n----- RELEASE TEST DB CONNECTION POOL\n')


@pytest.fixture(scope='function')
def session(request, db):
    session = db['session_factory']()
    yield session
    print('\n----- CREATE DB SESSION\n')

    session.rollback()
    session.close()
    print('\n----- ROLLBACK DB SESSION\n')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)