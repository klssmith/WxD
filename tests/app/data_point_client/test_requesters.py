import redis

from app.datapoint_client.requesters import CacheRequester


from freezegun import freeze_time
# EXTERNAL REQUESTER TESTS
# def test_datapoint_client_build_url_and_payload(mocker):
#     client = DatapointClient('123', mocker.Mock(), mocker.Mock())
#     url, payload = client.build_url_and_payload('hourly', 'wxfcs', 1000)

#     assert url == client.BASE_URL + 'val/wxfcs/all/json/1000'
#     assert payload == {'key': client.api_key, 'res': 'hourly'}


# def test_datapoint_client_make_request(mocker):
#     client = DatapointClient('123', mocker.Mock(), mocker.Mock())
#     url = 'http://www.example.com'
#     payload = {'key': client.api_key, 'res': 'hourly'}

#     with requests_mock.Mocker() as m:
#         m.get(
#             '{url}?key={api_key}&res={res}'.format(url=url, api_key=payload['key'], res=payload['res']),
#             complete_qs=True,
#             json="the weather"
#         )
#         response = client.make_request('http://www.example.com/', payload)

#     assert response == 'the weather'


# def test_datapoint_client_make_request_when_bad_status_code_returned(mocker):
#     client = DatapointClient('123', mocker.Mock(), mocker.Mock())
#     url = 'http://www.example.com'
#     payload = {'key': client.api_key, 'res': 'hourly'}

#     with pytest.raises(requests.exceptions.HTTPError) as e, requests_mock.Mocker() as m:
#         m.get(
#             '{url}?key={api_key}&res={res}'.format(url=url, api_key=payload['key'], res=payload['res']),
#             complete_qs=True,
#             status_code=403
#         )
#         client.make_request('http://www.example.com/', payload)

#     assert m.called
#     assert '403 Client Error' in str(e.value)


# CACHE REQUESTER TESTS

class MockExternalRequester:
    def __init__(self, api_key):
        pass

    def get_3hourly_forecasts(self, site):
        return 'the weather'

    def get_obs(self, site):
        return 'the obs'


def test_cache_requester_get_obs_when_obs_are_cached(mocker, site):
    mock_redis = mocker.patch('app.datapoint_client.requesters.redis.Redis.get', return_value='{"data": "obs"}')
    cache_requester = CacheRequester('123', external_requester=MockExternalRequester)

    assert cache_requester.get_obs(500) == {'data': 'obs'}


@freeze_time('2019-08-10 04:05')
def test_cache_requester_get_obs_when_obs_are_not_cached(mocker, site):
    mock_redis_get = mocker.patch('app.datapoint_client.requesters.redis.Redis.get', return_value=None)
    mock_redis_set = mocker.patch('app.datapoint_client.requesters.redis.Redis.set')
    cache_requester = CacheRequester('123', external_requester=MockExternalRequester)

    assert cache_requester.get_obs(500) == 'the obs'
    mock_redis_set.assert_called_once_with(500, '"the obs"', ex=3300)


def test_cache_requester_get_3hourly_forecasts():
    cache_requester = CacheRequester('123', external_requester=MockExternalRequester)

    assert cache_requester.get_3hourly_forecasts(500) == 'the weather'
