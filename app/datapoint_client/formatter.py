from collections import OrderedDict
from datetime import datetime

import pytz

from app.datapoint_client.definitions import FIELD_DESCRIPTORS, FORECAST_FIELD_DESCRIPTORS


class Formatter:
    definitions = {}

    def format(self, data):
        formatted_data = OrderedDict()

        for day in data:
            date = day['value']

            for rep in day["Rep"]:
                formatted_values = self.format_parameters(rep)
                date_time = self.format_time(date, rep['$'])
                formatted_data[date_time] = formatted_values

        return formatted_data

    def format_parameters(self, data):
        raise NotImplementedError()

    def format_time(self, day, mins):
        return datetime(
            int(day[0:4]),
            int(day[5:7]),
            int(day[8:10]),
            int(mins) // 60,
            tzinfo=pytz.utc
        )


class ObsFormatter(Formatter):

    def format_parameters(self, weather):
        formatted_values = {}

        for key, value in weather.items():
            if key == 'Pt':
                pressure_description, pressure = self.format_pt(value)
                formatted_values[pressure_description] = pressure
            elif key == 'W':
                weather_type, weather = self.format_wx(value)
                formatted_values[weather_type] = weather
            elif key == '$':
                continue
            else:
                formatted_values[FIELD_DESCRIPTORS[key]] = value

        return formatted_values

    def format_pt(self, pt_code):
        return self._format('Pt', pt_code)

    def format_wx(self, wx_code):
        return self._format('W', wx_code)

    def _format(self, descriptor, code):
        return (FIELD_DESCRIPTORS[descriptor]['description'], FIELD_DESCRIPTORS[descriptor].get(code, 'Unknown'))


class WeatherFormatter(Formatter):
    def format_parameters(self, weather):
        formatted_values = {}

        for key, value in weather.items():
            if key == 'V':
                visibility_description, visibility = self.format_visibility(value)
                formatted_values[visibility_description] = visibility
            elif key == 'W':
                weather_type, weather = self.format_wx(value)
                formatted_values[weather_type] = weather
            elif key == '$':
                continue
            else:
                formatted_values[FORECAST_FIELD_DESCRIPTORS[key]] = value

        return formatted_values

    def format_visibility(self, vis):
        return self._format('V', vis)

    def format_wx(self, wx_code):
        return self._format('W', wx_code)

    def _format(self, descriptor, code):
        return (FORECAST_FIELD_DESCRIPTORS[descriptor]['description'],
                FORECAST_FIELD_DESCRIPTORS[descriptor].get(code, 'Unknown'))
