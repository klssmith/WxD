import pytest

from app import create_app
from app.datapoint_client.client import DatapointClient
from app.models import Site


@pytest.fixture(scope='session')
def test_client():
    """Returns a test client"""
    app = create_app()
    app.testing = True

    with app.test_request_context():
        yield app.test_client()


@pytest.fixture(scope='session')
def dp_client():
    """Returns a DatapointClient with a fake API key"""
    return DatapointClient('api-key')


@pytest.fixture(scope='session')
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
