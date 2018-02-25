from datetime import datetime

import requests_mock

from app.datapoint_client.client import DatapointClient
from tests.json_response_fixtures.all_obs_for_site import obs_json


def test_get_all_obs_json_hits_the_correct_endpoint():
    client = DatapointClient('fake-key')
    site = 1000

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json={"status": "success"}
        )

        client._get_all_obs_json(site)

    assert m.called


def test_get_all_obs_for_site_returns_an_entry_for_each_ob_in_the_expected_format():
    client = DatapointClient('fake-key')
    site = 3772

    with requests_mock.Mocker() as m:
        m.get(
            'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/{}?res=hourly&key={}'.format(
             site, client.api_key),
            json=obs_json
        )
        result = client.get_all_obs_for_site(site)

    assert len(result) == 3
    assert result.keys() == {datetime(2018, 3, 2, 23, 0), datetime(2018, 3, 3, 0, 0), datetime(2018, 3, 3, 1, 0)}
    assert result[datetime(2018, 3, 3, 0, 0)] == {
        'W': '8', 'S': '9', 'Pt': 'F', 'P': '992', 'V': '2700', 'Dp': '-0.2', 'H': '95.0', 'T': '0.5', 'D': 'ENE'
    }
