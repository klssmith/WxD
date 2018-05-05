from collections import OrderedDict

from bs4 import BeautifulSoup
import requests_mock
import pytest

from flask import url_for

from app.datapoint_client.errors import SiteError
from tests.json_fixtures.all_obs_for_site import obs_json


def test_all_site_observations_each_site_name_links_to_its_obs_page(mocker, test_client):
    mock_site_list = OrderedDict([('Capel Curig', 3305), ('Scampton', 3373)])
    mocker.patch('app.views.SITE_CODES', mock_site_list)
    response = test_client.get(url_for('all_site_observations'))
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    link_one = page.find('a', string='Capel Curig')
    assert link_one['href'] == '/observations/3305'

    link_two = page.find('a', string='Scampton')
    assert link_two['href'] == '/observations/3373'


def test_get_site_observation_returns_200_with_valid_site_id(mocker, test_client, site):
    mocker.patch('app.datapoint_client.client.DatapointClient.get_all_obs_for_site')
    mocker.patch('app.views.dao_get_site_by_id', return_value=site)

    response = test_client.get(url_for('site_observation', site_id=site.id))

    assert response.status_code == 200


def test_site_observation_shows_the_site_name(mocker, dp_client, test_client, site):
    mocker.patch('app.views.DatapointClient', return_value=dp_client)
    mocker.patch('app.views.dao_get_site_by_id', return_value=site)

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site.id, dp_client.api_key),
            json=obs_json
        )

        response = test_client.get(url_for('site_observation', site_id=site.id))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.find('h1').string == 'Weather Observations for Lochaven'


def test_site_observation_displays_obs_in_a_table(mocker, dp_client, test_client, site):
    mocker.patch('app.views.DatapointClient', return_value=dp_client)
    mocker.patch('app.views.dao_get_site_by_id', return_value=site)

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site.id, dp_client.api_key),
            json=obs_json
        )

        response = test_client.get(url_for('site_observation', site_id=site.id))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    dates = page.tbody.find_all('th')
    assert dates[0].string == '2018-03-02 23:00:00'
    assert dates[1].string == '2018-03-03 00:00:00'
    assert dates[2].string == '2018-03-03 01:00:00'

    weather_obs = page.tbody.tr.find_all('td')
    assert weather_obs[0].string == 'Mist'
    assert weather_obs[4].string == '11 E'
    assert weather_obs[5].string is None


def test_get_site_observation_returns_404_with_invalid_site_id(mocker, test_client):
    mocker.patch('app.datapoint_client.client.DatapointClient.get_all_obs_for_site', side_effect=SiteError)
    site_mock = mocker.patch('app.views.dao_get_site_by_id')

    response = test_client.get(url_for('site_observation', site_id=1000))

    site_mock.assert_not_called()
    assert response.status_code == 404


@pytest.mark.parametrize('status_code,page_heading', [
    (403, 'Forbidden'),
    (404, 'Page not found'),
    (500, 'Something went wrong'),
])
def test_error_pages(mocker, dp_client, test_client, status_code, page_heading):
    mocker.patch('app.views.DatapointClient', return_value=dp_client)
    site_mock = mocker.patch('app.views.dao_get_site_by_id')

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             1000, dp_client.api_key),
            status_code=status_code
        )

        response = test_client.get(url_for('site_observation', site_id=1000))

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    site_mock.assert_not_called()
    assert page.title.string == 'WxD'
    assert page.h1.string == page_heading
    assert response.status_code == status_code
