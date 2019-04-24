from datetime import datetime

import pytest

from app.datapoint_client.formatter import Formatter, ObsFormatter, WeatherFormatter


class MockFormatter(Formatter):
    def format_parameters(self, data):
        return data


# Formatter tests:
def test_formatter_is_an_abstract_class_that_formats_data():
    with pytest.raises(NotImplementedError):
        Formatter().format(original_obs_data)


def test_formatter_formats_parameters_the_correct_number_of_times(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_parameters')

    assert f.format_parameters.call_count == 0
    f.format(original_obs_data)

    assert f.format_parameters.call_count == 3


def test_formatter_formats_time_the_correct_number_of_times(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_time')

    assert f.format_time.call_count == 0
    f.format(original_obs_data)

    assert f.format_time.call_count == 3


@pytest.mark.parametrize('day, minutes, expected_result', [
    ('2019-04-08Z', '0', datetime(2019, 4, 8, 0, 0)),
    ('2019-04-08Z', '960', datetime(2019, 4, 8, 16, 0)),

])
def test_formatter_formats_time(day, minutes, expected_result):
    assert Formatter().format_time(day, minutes) == expected_result


# ObsFormatter tests:
def test_obs_formatter_formats_observation():
    f = ObsFormatter()

    result = f.format(original_obs_data)

    assert len(result) == 3
    assert result[datetime(2019, 4, 8, 12, 0)] == {
        'Wind Direction': 'NNW',
        'Screen Relative Humidity': '87.5',
        'Pressure': '1010', 'Wind Speed': '2',
        'Temperature': '11.3', 'Visibility': '3300',
        'Weather Type': 'Overcast',
        'Pressure Tendency': 'Rising',
        'Dew Point': '9.3'}


def test_obs_formatter_formats_pressure_tendency():
    assert ObsFormatter().format_pt('R') == ('Pressure Tendency', 'Rising')


def test_obs_formatter_formats_weather():
    assert ObsFormatter().format_wx('27') == ('Weather Type', 'Heavy snow')


# WeatherFormatter tests
def test_wx_formatter_formats_forecast():
    f = WeatherFormatter()

    result = f.format(original_fx_data)

    assert len(result) == 4
    assert result[datetime(2019, 4, 23, 21, 0)] == {
        'Wind Direction': 'E',
        'Feels Like Temperature': '14',
        'Wind Gust': '13',
        'Screen Relative Humidity': '62',
        'Precipitation Probability': '4',
        'Wind Speed': '7',
        'Temperature': '15',
        'Visibility': 'Good - Between 10-20 km',
        'Weather Type': 'Cloudy',
        'Max UV Index': '0'
    }


def test_wx_formatter_formats_visibility():
    assert WeatherFormatter().format_visibility('EX') == ('Visibility', 'Excellent - More than 40 km')


def test_wx_formatter_formats_weather():
    assert WeatherFormatter().format_wx('15') == ('Weather Type', 'Heavy rain')


original_obs_data = [{
    'type': 'Day',
    'value': '2019-04-08Z',
    'Rep': [{
        'D': 'NNW',
        'H': '87.5',
        'P': '1010',
        'S': '2',
        'T': '11.3',
        'V': '3300',
        'W': '8',
        'Pt': 'R',
        'Dp': '9.3',
        '$': '720'
    }, {
        'D': 'WSW',
        'H': '76.8',
        'P': '1010',
        'S': '6',
        'T': '14.4',
        'V': '4000',
        'W': '3',
        'Pt': 'F',
        'Dp': '10.4',
        '$': '960'
    }]
}, {
    'type': 'Day',
    'value': '2019-04-09Z',
    'Rep': [{
        'D': 'ENE',
        'H': '100.0',
        'P': '1012',
        'S': '7',
        'T': '7.4',
        'V': '100',
        'W': '6',
        'Pt': 'R',
        'Dp': '7.4',
        '$': '0'
    }]
}]


original_fx_data = [{
    'type': 'Day',
    'value': '2019-04-23Z',
    'Rep': [{
        'D': 'E',
        'F': '14',
        'G': '13',
        'H': '62',
        'Pp': '4',
        'S': '7',
        'T': '15',
        'V': 'GO',
        'W': '7',
        'U': '0',
        '$': '1260',
    }],
  }, {
    'type': 'Day',
    'value': '2019-04-24Z',
    'Rep': [{
        'D': 'NE',
        'F': '13',
        'G': '9',
        'H': '74',
        'Pp': '3',
        'S': '4',
        'T': '13',
        'V': 'GO',
        'W': '7',
        'U': '0',
        '$': '0',
    }, {
        'D': 'S',
        'F': '12',
        'G': '29',
        'H': '80',
        'Pp': '58',
        'S': '16',
        'T': '15',
        'V': 'GO',
        'W': '14',
        'U': '4',
        '$': '720',
        }],
}, {
    'type': 'Day',
    'value': '2019-04-25Z',
    'Rep': [{
        'D': 'SE',
        'F': '8',
        'G': '18',
        'H': '81',
        'Pp': '4',
        'S': '9',
        'T': '10',
        'V': 'VG',
        'W': '2',
        'U': '0',
        '$': '0',
    }],
 }]
