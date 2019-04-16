from collections import OrderedDict
from datetime import datetime

from app.datapoint_client.definitions import FIELD_DESCRIPTORS, PRESSURE_TENDENCY_DESCRIPTORS, WX_DESCRIPTORS


class Formatter:
    def format_observation(self, data):
        formatted_data = OrderedDict()

        for day in data:
            date = day['value']

            for rep in day["Rep"]:
                formatted_values = self._format_obs_parameters(rep)
                date_time = self.format_time(date, rep['$'])
                formatted_data[date_time] = formatted_values

        return formatted_data

    def _format_obs_parameters(self, weather):
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

    def format_time(self, data, rep):
        raise NotImplementedError()

    def format_pt(self, data):
        raise NotImplementedError()

    def format_wx(self, data):
        raise NotImplementedError()


class ObsFormatter(Formatter):
    def format_time(self, day, mins):
        return datetime(
            int(day[0:4]),
            int(day[5:7]),
            int(day[8:10]),
            int(mins) // 60
        )

    def format_pt(self, pt_code):
        return ('Pressure Tendency', PRESSURE_TENDENCY_DESCRIPTORS.get(pt_code, 'Unknown'))

    def format_wx(self, wx_code):
        return ('Weather Type', WX_DESCRIPTORS.get(wx_code, 'Unknown'))
