from bs4 import BeautifulSoup

from flask import url_for


def test_site_details_nav_for_site_with_obs(test_client, obs_site):
    response = test_client.get(url_for('main.site', site_id=obs_site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_nav = page.find('ul', class_='list-group-horizontal').find_all('a')
    assert [i for i in site_nav] == [url_for()]
    assert False


def test_site_details_nav_for_site_without_obs(test_client, site):
    pass


def test_forecast_single_site_nav_for_site_with_obs(test_client, obs_site):
    pass


def test_forecast_single_site_nav_for_site_without_obs(test_client, site):
    pass


def test_observation_single_site_nav(test_client, obs_site):
    pass
