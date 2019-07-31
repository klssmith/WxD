from bs4 import BeautifulSoup
from flask import url_for
import pytest

from app.main.views import ShowSingleForecast, ShowSingleOb


def test_site_details_nav_for_site_with_obs(test_client, obs_site):
    response = test_client.get(url_for('main.site', site_id=obs_site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_nav = page.find('ul', class_='list-group-horizontal').find_all('li')
    assert len(site_nav) == 3

    assert site_nav[0].a.text == 'About the site'
    assert site_nav[0].a['href'] == url_for('main.site', site_id=obs_site.id)

    assert site_nav[1].a.text == 'Forecast'
    assert site_nav[1].a['href'] == url_for('main.site_forecast', site_id=obs_site.id)

    assert site_nav[2].a.text == 'Observations'
    assert site_nav[2].a['href'] == url_for('main.site_observation', site_id=obs_site.id)


def test_site_details_nav_for_site_without_obs(test_client, site):
    response = test_client.get(url_for('main.site', site_id=site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_nav = page.find('ul', class_='list-group-horizontal').find_all('li')
    assert len(site_nav) == 2

    assert site_nav[0].a.text == 'About the site'
    assert site_nav[0].a['href'] == url_for('main.site', site_id=site.id)

    assert site_nav[1].a.text == 'Forecast'
    assert site_nav[1].a['href'] == url_for('main.site_forecast', site_id=site.id)


def test_forecast_single_site_nav_for_site_with_obs(mocker, test_client, obs_site):
    mocker.patch.object(ShowSingleForecast, 'get_data')
    response = test_client.get(url_for('main.site_forecast', site_id=obs_site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_nav = page.find('ul', class_='list-group-horizontal').find_all('li')
    assert len(site_nav) == 3

    assert site_nav[0].a.text == 'About the site'
    assert site_nav[0].a['href'] == url_for('main.site', site_id=obs_site.id)

    assert site_nav[1].a.text == 'Forecast'
    assert site_nav[1].a['href'] == url_for('main.site_forecast', site_id=obs_site.id)

    assert site_nav[2].a.text == 'Observations'
    assert site_nav[2].a['href'] == url_for('main.site_observation', site_id=obs_site.id)


def test_forecast_single_site_nav_for_site_without_obs(mocker, test_client, site):
    mocker.patch.object(ShowSingleForecast, 'get_data')
    response = test_client.get(url_for('main.site_forecast', site_id=site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_nav = page.find('ul', class_='list-group-horizontal').find_all('li')
    assert len(site_nav) == 2

    assert site_nav[0].a.text == 'About the site'
    assert site_nav[0].a['href'] == url_for('main.site', site_id=site.id)

    assert site_nav[1].a.text == 'Forecast'
    assert site_nav[1].a['href'] == url_for('main.site_forecast', site_id=site.id)


def test_observation_single_site_nav(mocker, test_client, obs_site):
    mocker.patch.object(ShowSingleOb, 'get_data')
    response = test_client.get(url_for('main.site_observation', site_id=obs_site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_nav = page.find('ul', class_='list-group-horizontal').find_all('li')
    assert len(site_nav) == 3

    assert site_nav[0].a.text == 'About the site'
    assert site_nav[0].a['href'] == url_for('main.site', site_id=obs_site.id)

    assert site_nav[1].a.text == 'Forecast'
    assert site_nav[1].a['href'] == url_for('main.site_forecast', site_id=obs_site.id)

    assert site_nav[2].a.text == 'Observations'
    assert site_nav[2].a['href'] == url_for('main.site_observation', site_id=obs_site.id)


@pytest.mark.parametrize('endpoint, highlighted_nav', [
    ('main.site', 'About the site'),
    ('main.site_forecast', 'Forecast'),
    ('main.site_observation', 'Observations'),
])
def test_highlights_the_menu_item_for_the_page(mocker, test_client, obs_site, endpoint, highlighted_nav):
    mocker.patch.object(ShowSingleForecast, 'get_data')
    mocker.patch.object(ShowSingleOb, 'get_data')

    response = test_client.get(url_for(endpoint, site_id=obs_site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    highlighted_nav_item = page.find('ul', class_='list-group-horizontal').find('li', class_='list-group-item-info')
    assert highlighted_nav_item.text.strip() == highlighted_nav
