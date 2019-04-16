from datetime import datetime

import pytest

from app.datapoint_client.formatter import Formatter, ObsFormatter


class MockFormatter(Formatter):
    def format_time(self, data, other):
        return data

    def format_wx(self, data):
        return data, 'data'

    def format_pt(self, data):
        return data, 'data'


# Formatter tests:
def test_formatter_is_an_abstract_class_that_formats_data():
    with pytest.raises(NotImplementedError):
        Formatter().format_observation(original_data)


def test_formatter_formats_time_using_format_time(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_time')

    assert f.format_time.call_count == 0
    f.format_observation(original_data)

    assert f.format_time.call_count == 3


def test_formatter_formats_pressure_tendency_using_format_pt(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_pt')

    assert f.format_pt.call_count == 0
    f.format_observation(original_data)

    assert f.format_pt.call_count == 3


def test_formatter_formats_weather_description_using_format_wx(mocker):
    f = MockFormatter()
    mocker.spy(f, 'format_wx')

    assert f.format_wx.call_count == 0
    f.format_observation(original_data)

    assert f.format_wx.call_count == 3


# ObsFormatter tests:
def test_obs_formatter_formats_observation():
    f = ObsFormatter()

    result = f.format_observation(original_data)

    assert len(result) == 3
    assert result[datetime(2019, 4, 8, 12, 0)] == {
        'Wind Direction': 'NNW',
        'Screen Relative Humidity': '87.5',
        'Pressure': '1010', 'Wind Speed': '2',
        'Temperature': '11.3', 'Visibility': '3300',
        'Weather Type': 'Overcast',
        'Pressure Tendency': 'Rising',
        'Dew Point': '9.3'}


@pytest.mark.parametrize('day, minutes, expected_result', [
    ('2019-04-08Z', '0', datetime(2019, 4, 8, 0, 0)),
    ('2019-04-08Z', '960', datetime(2019, 4, 8, 16, 0)),

])
def test_obs_formatter_formats_time(day, minutes, expected_result):
    assert ObsFormatter().format_time(day, minutes) == expected_result


def test_obs_formatter_formats_pressure_tendency():
    assert ObsFormatter().format_pt('R') == ('Pressure Tendency', 'Rising')


def test_obs_formatter_formats_pressure_weather():
    assert ObsFormatter().format_wx('27') == ('Weather Type', 'Heavy snow')


original_data = [{
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
