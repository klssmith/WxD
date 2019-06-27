from datetime import datetime

import pytest
import pytz

from app.datapoint_client.formatter import Formatter, ObsFormatter, WeatherFormatter
from tests.json_fixtures.all_obs_for_site import obs_json
from tests.json_fixtures.forecast_for_site import three_hourly_fx_json


obs_data = obs_json['SiteRep']['DV']['Location']['Period']
fx_data = three_hourly_fx_json['SiteRep']['DV']['Location']['Period']


class MockFormatter(Formatter):
    def format_parameters(self, data):
        return data


# Formatter tests:
def test_formatter_is_an_abstract_class_that_formats_data():
    with pytest.raises(NotImplementedError):
        Formatter().format(obs_data)


def test_formatter_formats_parameters_the_correct_number_of_times(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_parameters')

    assert f.format_parameters.call_count == 0
    f.format(obs_data)

    assert f.format_parameters.call_count == 3


def test_formatter_formats_time_the_correct_number_of_times(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_time')

    assert f.format_time.call_count == 0
    f.format(obs_data)

    assert f.format_time.call_count == 3


@pytest.mark.parametrize('day, minutes, expected_result', [
    ('2019-04-08Z', '0', datetime(2019, 4, 8, 0, 0, tzinfo=pytz.utc)),
    ('2019-04-08Z', '960', datetime(2019, 4, 8, 16, 0, tzinfo=pytz.utc)),

])
def test_formatter_formats_time(day, minutes, expected_result):
    assert Formatter().format_time(day, minutes) == expected_result


# ObsFormatter tests:
def test_obs_formatter_formats_observation():
    f = ObsFormatter()

    result = f.format(obs_data)

    assert len(result) == 3
    assert result[datetime(2018, 3, 3, 0, 0, tzinfo=pytz.utc)] == {
        'Wind Direction': 'ENE',
        'Screen Relative Humidity': '95.0',
        'Pressure': '992',
        'Wind Speed': '9',
        'Temperature': '0.5',
        'Visibility': '2700',
        'Weather Type': 'Overcast',
        'Pressure Tendency': 'Falling',
        'Dew Point': '-0.2'}


def test_obs_formatter_formats_pressure_tendency():
    assert ObsFormatter().format_pt('R') == ('Pressure Tendency', 'Rising')


def test_obs_formatter_formats_weather():
    assert ObsFormatter().format_wx('27') == ('Weather Type', 'Heavy snow')


# WeatherFormatter tests
def test_wx_formatter_formats_forecast():
    f = WeatherFormatter()

    result = f.format(fx_data)

    assert len(result) == 3
    assert result[datetime(2019, 4, 28, 18, 0, tzinfo=pytz.utc)] == {
        'Wind Direction': 'NNE',
        'Feels Like Temperature': '12',
        'Wind Gust': '16',
        'Screen Relative Humidity': '58',
        'Precipitation Probability': '0',
        'Wind Speed': '11',
        'Temperature': '14',
        'Visibility': 'Good - Between 10-20 km',
        'Weather Type': 'Partly cloudy (day)',
        'Max UV Index': '1'
    }


def test_wx_formatter_formats_visibility():
    assert WeatherFormatter().format_visibility('EX') == ('Visibility', 'Excellent - More than 40 km')


def test_wx_formatter_formats_weather():
    assert WeatherFormatter().format_wx('15') == ('Weather Type', 'Heavy rain')
