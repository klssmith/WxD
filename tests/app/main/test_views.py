import re

from bs4 import BeautifulSoup
import requests_mock
import pytest

from flask import url_for

from app import db
from app.datapoint_client.errors import SiteError
from app.models import Site
from tests.json_fixtures.all_obs_for_site import obs_json
from tests.json_fixtures.forecast_for_site import three_hourly_fx_json


def test_all_site_observations_each_site_name_links_to_its_obs_page(test_client, test_db_session):
    site_1 = Site(id=1, name='Farley Down', observations=True)
    site_2 = Site(id=2, name='Little Borwood', observations=True)

    db.session.add_all([site_1, site_2])
    db.session.commit()

    response = test_client.get(url_for('main.all_site_observations'))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    link_one = page.find('a', string='Farley Down')
    assert link_one['href'] == url_for('main.site_observation',  site_id=1)

    link_two = page.find('a', string='Little Borwood')
    assert link_two['href'] == url_for('main.site_observation',  site_id=2)


def test_site_observation_shows_the_site_name(mocker, dp_client, test_client, site):
    mocker.patch('app.main.views.client', new=dp_client)

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site.id, dp_client.api_key),
            json=obs_json
        )

        response = test_client.get(url_for('main.site_observation', site_id=site.id))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert response.status_code == 200
    assert page.find('h1').string == 'Lochaven - Observations'


def test_site_observation_displays_obs_in_a_table(mocker, dp_client, test_client, site):
    mocker.patch('app.main.views.client', new=dp_client)

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site.id, dp_client.api_key),
            json=obs_json
        )

        response = test_client.get(url_for('main.site_observation', site_id=site.id))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    dates_and_times = page.tbody.find_all('th')
    assert len(dates_and_times) == 6

    assert dates_and_times[0].string == 'Friday 02 Mar'
    assert dates_and_times[1].string == '11pm'
    assert dates_and_times[2].string == 'Saturday 03 Mar'
    assert dates_and_times[3].string == '12am'
    assert dates_and_times[4].string is None
    assert dates_and_times[5].string == '1am'

    weather_obs = page.tbody.tr.find_all('td')
    assert weather_obs[0].string == 'Mist'
    assert weather_obs[4].string == '11'
    assert weather_obs[5].string is None


def test_get_site_observation_returns_404_with_invalid_site_id(mocker, test_client):
    mocker.patch('app.datapoint_client.client.DatapointClient.get_obs_for_site', side_effect=SiteError)
    site_mock = mocker.patch('app.main.views.dao_get_site_by_id')

    response = test_client.get(url_for('main.site_observation', site_id=1000))

    site_mock.assert_not_called()
    assert response.status_code == 404


@pytest.mark.parametrize('obs_query_string, expected_dao_function', [
    ('true', 'dao_find_observation_sites_by_name'),
    ('', 'dao_find_sites_by_name'),
])
def test_results_calls_the_expected_dao_function(
    mocker,
    test_client,
    obs_site,
    obs_query_string,
    expected_dao_function,
):
    dao_mock = mocker.patch('app.main.views.{}'.format(expected_dao_function))

    search_term = 'silverley'
    test_client.get(
        url_for('main.results'),
        query_string={'search-term': search_term, 'obs': obs_query_string, 'link': 'site'})

    dao_mock.assert_called_once_with(search_term)


@pytest.mark.parametrize('link_query_string, expected_page_link, expected_back_link', [
    ('site', 'main.site', 'main.index'),
    ('obs', 'main.site_observation', 'main.all_site_observations'),
    ('fx', 'main.site_forecast', 'main.all_site_forecasts'),
])
def test_results_displays_the_links_on_the_page(
    mocker,
    test_client,
    site,
    link_query_string,
    expected_page_link,
    expected_back_link,
):
    mocker.patch('app.main.views.dao_find_sites_by_name', return_value=[site])
    response = test_client.get(
        url_for('main.results'),
        query_string={'search-term': 'loch', 'link': link_query_string})
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert len(page.find('p').find_all('a')) == 1

    site_link = page.find('a', string='Lochaven')
    assert site_link['href'] == url_for(expected_page_link,  site_id=99)

    back_link = page.find('a', string='Back')
    assert back_link['href'] == url_for(expected_back_link)


def test_results_displays_message_when_no_results_are_found(mocker, test_client):
    mocker.patch('app.main.views.dao_find_observation_sites_by_name', return_value=[])
    response = test_client.get(url_for('main.results'), query_string={'search-term': 'lilliput', 'link': 'obs'})
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.find('p').string == "We couldn't find that site."


def test_all_site_forecasts_shows_each_site_name_and_links_to_its_page(test_client, test_db_session):
    site_1 = Site(id=1, name='Farley Down')
    site_2 = Site(id=2, name='Little Borwood', observations=True)

    db.session.add_all([site_1, site_2])
    db.session.commit()

    response = test_client.get(url_for('main.all_site_forecasts'))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    link_one = page.find('a', string='Farley Down')
    assert link_one['href'] == url_for('main.site_forecast',  site_id=1)

    link_two = page.find('a', string='Little Borwood')
    assert link_two['href'] == url_for('main.site_forecast',  site_id=2)


def test_site_forecast_shows_the_site_name(mocker, dp_client, test_client, site):
    mocker.patch('app.main.views.client', new=dp_client)

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{}?res=3hourly&key={}'.format(
             site.id, dp_client.api_key),
            json=three_hourly_fx_json
        )

        response = test_client.get(url_for('main.site_forecast', site_id=site.id))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert response.status_code == 200
    assert page.find('h1').string == 'Lochaven - Forecast'


def test_site_forecast_displays_forecast_in_a_table(mocker, dp_client, test_client, site):
    mocker.patch('app.main.views.client', new=dp_client)

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{}?res=3hourly&key={}'.format(
             site.id, dp_client.api_key),
            json=three_hourly_fx_json
        )

        response = test_client.get(url_for('main.site_forecast', site_id=site.id))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    dates_and_times = page.tbody.find_all('th')
    assert len(dates_and_times) == 6

    assert dates_and_times[0].string == 'Sunday 28 Apr'
    assert dates_and_times[1].string == '7pm'
    assert dates_and_times[2].string is None
    assert dates_and_times[3].string == '10pm'
    assert dates_and_times[4].string == 'Monday 29 Apr'
    assert dates_and_times[5].string == '1am'

    forecast = page.tbody.tr.find_all('td')
    assert forecast[0].string == 'Partly cloudy (day)'
    assert forecast[3].string == '58'
    assert forecast[7].string == 'Good - Between 10-20 km'


def test_get_site_forecast_returns_404_with_invalid_site_id(mocker, test_client):
    mocker.patch('app.datapoint_client.client.DatapointClient.get_3hourly_forecasts_for_site', side_effect=SiteError)
    site_mock = mocker.patch('app.main.views.dao_get_site_by_id')

    response = test_client.get(url_for('main.site_forecast', site_id=1000))

    site_mock.assert_not_called()
    assert response.status_code == 404


@pytest.mark.parametrize('status_code,page_heading', [
    (403, 'Forbidden'),
    (404, 'Page not found'),
    (500, 'Something went wrong'),
])
def test_error_pages(mocker, dp_client, test_client, status_code, page_heading):
    mocker.patch('app.main.views.client', new=dp_client)
    site_mock = mocker.patch('app.main.views.dao_get_site_by_id')

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             1000, dp_client.api_key),
            status_code=status_code
        )

        response = test_client.get(url_for('main.site_observation', site_id=1000))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_mock.assert_not_called()
    assert page.title.string == 'WxD'
    assert page.h1.string == page_heading
    assert response.status_code == status_code


def test_site_details_for_site_with_observations(test_client, obs_site):
    response = test_client.get(url_for('main.site', site_id=obs_site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.find(id='mapid')
    assert page.find(id='overview-map-id')

    assert page.find(lambda tag: tag.name == 'p' and tag.text == 'Latitude: {}'.format(obs_site.latitude))
    assert page.find(lambda tag: tag.name == 'p' and tag.text == 'Longitude: {}'.format(obs_site.longitude))
    assert page.find(lambda tag: tag.name == 'p' and tag.text == 'Elevation: {} m'.format(obs_site.elevation))

    # assert page.find('a', string=re.compile('Silverley observations'))
    # assert page.find('a', string=re.compile('Silverley forecast'))


def test_site_details_for_site_without_observations(test_client, site):
    response = test_client.get(url_for('main.site', site_id=site.id))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.find(id='mapid')
    assert page.find(id='overview-map-id')

    assert page.find(lambda tag: tag.name == 'p' and tag.text == 'Latitude: {}'.format(site.latitude))
    assert page.find(lambda tag: tag.name == 'p' and tag.text == 'Longitude: {}'.format(site.longitude))
    assert page.find(lambda tag: tag.name == 'p' and tag.text == 'Elevation: {} m'.format(site.elevation))

    # assert not page.find('a', string=re.compile('Lochaven observations'))
    # assert page.find('a', string=re.compile('Lochaven forecast'))
