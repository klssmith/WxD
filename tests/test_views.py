from flask import url_for

from app.datapoint_client.errors import SiteError


def test_get_site_observation_returns_200_with_valid_site_id(mocker, test_client):
    mocker.patch('app.datapoint_client.client.DatapointClient.get_all_obs_for_site')
    response = test_client.get(url_for('site_observation', site_id=3772))

    assert response.status_code == 200


def test_get_site_observation_returns_404_with_invalid_site_id(mocker, test_client):
    mocker.patch('app.datapoint_client.client.DatapointClient.get_all_obs_for_site', side_effect=SiteError)
    response = test_client.get(url_for('site_observation', site_id=1000))

    assert response.status_code == 404
