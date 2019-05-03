import pytest

from app import db
from app.models import Site
from app.site_dao import (
    dao_find_observation_sites_by_name,
    dao_get_all_sites,
    dao_get_all_sites_with_observations,
    dao_get_site_by_id,
)


def test_dao_get_all_sites(test_db_session):
    site_g = Site(id=5, name='Golf')
    obs_site_f = Site(id=1, name='Foxtrot', observations=True)
    obs_site_a = Site(id=17, name='Alpha', observations=True)
    site_k = Site(id=10, name='Kilo')

    db.session.add_all([site_g, obs_site_f, obs_site_a, site_k])
    db.session.commit()

    result = dao_get_all_sites()

    assert len(result) == 4
    assert result[0].name == 'Alpha'
    assert result[1].name == 'Foxtrot'
    assert result[2].name == 'Golf'
    assert result[3].name == 'Kilo'


def test_dao_get_site_by_id_when_site_exists(site):
    assert dao_get_site_by_id(site.id) == site


def test_dao_get_site_by_id_when_site_is_not_found(test_db_session):
    assert dao_get_site_by_id(1) is None


def test_dao_get_all_sites_with_observations_returns_obs_sites(test_db_session):
    site_g = Site(id=5, name='Golf')
    obs_site_f = Site(id=1, name='Foxtrot', observations=True)
    site_i = Site(id=73, name='India', observations=False)
    obs_site_a = Site(id=17, name='Alpha', observations=True)
    obs_site_m = Site(id=56, name='Mike', observations=True)
    site_k = Site(id=10, name='Kilo')

    db.session.add_all([site_g, obs_site_f, site_i, obs_site_a, obs_site_m, site_k])
    db.session.commit()

    result = dao_get_all_sites_with_observations()

    assert len(result) == 3
    assert result[0].name == 'Alpha'
    assert result[1].name == 'Foxtrot'
    assert result[2].name == 'Mike'


def test_dao_get_all_sites_with_observations_with_no_obs_sites():
    result = dao_get_all_sites_with_observations()
    assert result == []


def test_dao_find_observation_sites_by_name_with_no_match_returns_empty_list():
    result = dao_find_observation_sites_by_name('Billericay')
    assert result == []


def test_dao_find_observation_sites_by_name_when_site_is_not_obs_site_returns_empty_list(site):
    result = dao_find_observation_sites_by_name(site.name)
    assert result == []


@pytest.mark.parametrize('search_term', [
    'Silverley',
    'siLvErleY',
    'silver',
    'VerLey',
    'LEY',
])
def test_dao_find_observation_sites_by_name_returns_similar_search_terms(obs_site, search_term):
    result = dao_find_observation_sites_by_name(search_term)
    assert len(result) == 1
    assert result[0] == obs_site


def test_dao_find_observation_sites_by_name_can_return_multiple_matches(test_db_session):
    site_1 = Site(id=1, name='Fingrove', observations=True)
    site_2 = Site(id=2, name='Fingroove', observations=True)
    site_3 = Site(id=3, name='Fyngrove', observations=True)

    db.session.add_all([site_1, site_2, site_3])
    db.session.commit()

    result = dao_find_observation_sites_by_name('ngro')

    assert result == [site_2, site_1, site_3]
