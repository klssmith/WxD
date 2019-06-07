import pytest

from app import db
from app.datapoint_client.client import DatapointClient
from app.models import Site


@pytest.fixture
def dp_client():
    """Returns a DatapointClient with a fake API key"""
    return DatapointClient('api-key')


@pytest.fixture
def site(test_db_session):
    """Inserts a site without into the database and returns it"""
    site = Site(
        id=99,
        name='Lochaven',
        latitude=56.503,
        longitude=-4.332,
        elevation=995,
        region='he',
        unitary_auth_area='Highland',
        observations=False
    )
    db.session.add(site)
    db.session.commit()
    return site


@pytest.fixture
def obs_site(test_db_session):
    """Inserts a site with observations into the database and returns it"""
    site = Site(
        id=100,
        name='Silverley',
        latitude=51.148,
        longitude=0.661,
        elevation=10,
        region='se',
        unitary_auth_area='Kent',
        observations=True,
    )
    db.session.add(site)
    db.session.commit()
    return site
