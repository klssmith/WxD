import pytest

from app.datapoint_client.client import DatapointClient


@pytest.fixture(scope='session')
def client():
    """Creates a DatapointClient with a fake API key"""
    return DatapointClient('api-key')
