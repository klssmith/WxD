from collections import OrderedDict
from datetime import datetime

from app.datapoint_client.definitions import (
    FIELD_DESCRIPTORS,
    PRESSURE_TENDENCY_DESCRIPTORS,
    WX_DESCRIPTORS,
)


def format_observations(data):
    data = _add_datetime(data)
    data = _replace_obs_abbreviations(data)
    return data


def _add_datetime(data):
    od = OrderedDict()

    for day_dict in data:
        day = day_dict['value']
        for hour_dict in day_dict['Rep']:
            hour_dict_copy = hour_dict.copy()

            mins = int(hour_dict['$']) // 60
            dt = datetime(
                int(day[0:4]),
                int(day[5:7]),
                int(day[8:10]),
                mins
            )
            del hour_dict_copy['$']
            od[dt] = hour_dict_copy

    return od


def _replace_obs_abbreviations(observations):
    for date, wx_dict in observations.items():
        updated_values = {}

        for key, value in wx_dict.items():
            if key == 'Pt':
                updated_values[FIELD_DESCRIPTORS[key]] = PRESSURE_TENDENCY_DESCRIPTORS.get(value, 'Unknown')
            elif key == 'W':
                updated_values[FIELD_DESCRIPTORS[key]] = WX_DESCRIPTORS.get(value, 'Unknown')
            else:
                updated_values[FIELD_DESCRIPTORS[key]] = value
        observations[date] = updated_values

    return observations
