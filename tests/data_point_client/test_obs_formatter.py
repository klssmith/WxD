from collections import OrderedDict
from datetime import datetime

from app.datapoint_client.obs_formatter import format_observations, _add_datetime, _replace_obs_abbreviations


def test_format_observation():
    data = [{'value': '2018-03-14Z', 'type': 'Day', 'Rep': [{'T': '10.7', 'D': 'ESE', 'S': '17', 'Pt': 'F', 'V':
            '30000', 'P': '996', 'Dp': '3.7', '$': '1140', 'H': '61.9', 'W': '8'}, {'G': '30', 'T': '10.5', 'D': 'ESE',
             'S': '23', 'Pt': 'F', 'V': '35000', 'P': '995', 'Dp': '3.2', '$': '1200', 'H': '60.6', 'W': '8'}]},
            {'value': '2018-03-15Z', 'type': 'Day', 'Rep': [{'T': '9.8', 'D': 'ESE', 'S': '16', 'Pt': 'F', 'V':
             '40000', 'P': '990', 'Dp': '4.2', '$': '0', 'H': '68.2', 'W': '8'}]}]

    result = format_observations(data)

    assert len(result) == 3


def test_add_datetime_with_one_day():
    data = [
        {'value': '2018-03-13Z', 'type': 'Day', 'Rep':
            [{'T': '6.6', '$': '0', 'W': '7', 'H': '84.6', 'P': '999', 'S': '13', 'D': 'NW', 'V': '35000', 'Pt': 'R',
             'Dp': '4.2'}]
         }
    ]
    result = _add_datetime(data)

    assert result == OrderedDict([
        (datetime(2018, 3, 13, 0, 0),
         {'S': '13', 'H': '84.6', 'Dp': '4.2', 'T': '6.6', 'V': '35000', 'P': '999', 'D': 'NW', 'W': '7', 'Pt': 'R'})
    ])


def test_add_datetime_with_two_days():
    data = [
        {'value': '2018-03-12Z', 'type': 'Day', 'Rep': [
            {'T': '6.9', '$': '1380', 'W': '8', 'H': '84.0', 'P': '998', 'S': '8', 'D': 'NW', 'V': '50000', 'Pt': 'R',
             'Dp': '4.4'}]
         },
        {'value': '2018-03-13Z', 'type': 'Day', 'Rep': [
            {'T': '6.6', '$': '0', 'W': '7', 'H': '84.6', 'P': '999', 'S': '13', 'D': 'NW', 'V': '35000', 'Pt': 'R',
             'Dp': '4.2'},
            {'T': '6.4', '$': '60', 'W': '8', 'H': '85.8', 'P': '1000', 'S': '10', 'D': 'NW', 'V': '16000', 'Pt': 'R',
             'Dp': '4.2'}]
         }
    ]
    result = _add_datetime(data)

    assert result == OrderedDict([
        (datetime(2018, 3, 12, 23, 0),
         {'S': '8', 'H': '84.0', 'Dp': '4.4', 'T': '6.9', 'V': '50000', 'P': '998', 'D': 'NW', 'W': '8', 'Pt': 'R'}),
        (datetime(2018, 3, 13, 0, 0),
         {'S': '13', 'H': '84.6', 'Dp': '4.2', 'T': '6.6', 'V': '35000', 'P': '999', 'D': 'NW', 'W': '7', 'Pt': 'R'}),
        (datetime(2018, 3, 13, 1, 0),
         {'S': '10', 'H': '85.8', 'Dp': '4.2', 'T': '6.4', 'V': '16000', 'P': '1000', 'D': 'NW', 'W': '8', 'Pt': 'R'})
    ])


def test_replace_obs_abbreviations_replaces_all_abbreviations():
    data = OrderedDict([
     (datetime(2018, 3, 12, 20, 0),
      {'Pt': 'R', 'V': '17000', 'Dp': '5.6', 'D': 'WNW', 'P': '994', 'H': '87.8', 'W': '8', 'T': '7.5', 'S': '11'}),
     (datetime(2018, 3, 12, 21, 0),
      {'Pt': 'R', 'V': '18000', 'Dp': '5.2', 'D': 'NW', 'P': '996', 'H': '85.4', 'W': '7', 'T': '7.5', 'S': '10'}),
     (datetime(2018, 3, 12, 22, 0),
      {'Pt': 'R', 'V': '10000', 'Dp': '5.5', 'D': 'NNW', 'P': '997', 'H': '90.8', 'W': '11', 'T': '6.9', 'S': '10'})
    ])

    result = _replace_obs_abbreviations(data)

    assert len(result) == 3
    assert result[datetime(2018, 3, 12, 20, 0)] == {
        'Dew Point': '5.6',
        'Pressure': '994',
        'Pressure Tendency': 'Rising',
        'Screen Relative Humidity': '87.8',
        'Temperature': '7.5',
        'Visibility': '17000',
        'Weather Type': 'Overcast',
        'Wind Direction': 'WNW',
        'Wind Speed': '11'
    }


def test_replace_obs_abbreviations_replaces_unrecognised_pressure_tendency_with_unknown():
    data = OrderedDict([
        (datetime(2018, 3, 12, 20, 0),
         {'Pt': 'X', 'V': '17000', 'Dp': '5.6', 'D': 'WNW', 'P': '994', 'H': '87.8', 'W': '8', 'T': '7.5', 'S': '11'})
    ])

    result = _replace_obs_abbreviations(data)

    assert result[datetime(2018, 3, 12, 20, 0)]['Pressure Tendency'] == 'Unknown'


def test_replace_obs_abbreviations_replaces_unrecognised_weather_with_unknown():
    data = OrderedDict([
        (datetime(2018, 3, 12, 20, 0),
         {'Pt': 'R', 'V': '17000', 'Dp': '5.6', 'D': 'WNW', 'P': '994', 'H': '87.8', 'W': '99', 'T': '7.5', 'S': '11'})
    ])

    result = _replace_obs_abbreviations(data)

    assert result[datetime(2018, 3, 12, 20, 0)]['Weather Type'] == 'Unknown'
