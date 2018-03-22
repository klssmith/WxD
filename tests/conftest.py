import pytest

from app import app
from app.datapoint_client.client import DatapointClient


@pytest.fixture(scope='session')
def test_client():
    """Returns a test client"""
    app.testing = True

    with app.test_request_context():
        yield app.test_client()


@pytest.fixture(scope='session')
def dp_client():
    """Returns a DatapointClient with a fake API key"""
    return DatapointClient('api-key')
