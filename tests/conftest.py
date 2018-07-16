import os
import pytest

from alembic.command import upgrade
from alembic.config import Config

from app import create_app, db
from app.datapoint_client.client import DatapointClient
from app.models import Site


@pytest.fixture(scope='session')
def test_app():
    """Returns a new app for the whole test session"""
    app = create_app(test_mode=True)

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def test_client(test_app):
    with test_app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def test_db(test_app):
    assert 'wxd_test' in db.engine.url.database, 'Only run tests against the test database'

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ALEMBIC_CONFIG = os.path.join(BASE_DIR, 'migrations')
    config = Config(ALEMBIC_CONFIG + '/alembic.ini')
    config.set_main_option("script_location", ALEMBIC_CONFIG)

    upgrade(config, 'head')

    yield db

    db.session.remove()
    db.get_engine(test_app).dispose()


@pytest.fixture()
def test_db_session(test_db):
    yield test_db

    test_db.session.remove()
    for tbl in reversed(test_db.metadata.sorted_tables):
        test_db.engine.execute(tbl.delete())


@pytest.fixture()
def dp_client():
    """Returns a DatapointClient with a fake API key"""
    return DatapointClient('api-key')


@pytest.fixture()
def site():
    """Returns a mock site object"""
    return Site(
        id=1,
        name='Lochaven',
        latitude=56.503,
        longitude=-4.332,
        elevation=995,
        region='he',
        unitary_auth_area='Highland',
    )
