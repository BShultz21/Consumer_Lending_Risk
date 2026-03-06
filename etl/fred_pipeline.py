import requests
import json
import os

from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray


def get_api_key():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    key_path = os.path.join(project_root, "config", "api_config.json")

    with open(key_path) as f:
        key = json.load(f)['key']

    return key

class CallFredAPI:
    def __init__(self, key):
        self.key = key
        self.series = None
        self.url = f'https://api.stlouisfed.org/fred/series/observations?series_id={self.series}&realtime_start=1991-01-01&api_key={self.key}&file_type=json'

    def set_series(self, series):
        self.series = series

    def set_url(self):
        self.url = f'https://api.stlouisfed.org/fred/series/observations?series_id={self.series}&realtime_start=1991-01-01&api_key={self.key}&file_type=json'

    def get_historical_data(self, series):
        self.set_series(series)
        self.set_url()

        response = requests.get(self.url)
        if response.status_code == 200:
            self.parse_json_data(response.json())
        else:
            print(response.status_code)

    def parse_json_data(self, data):
        parsed_data = {}
        if self.series in ['DRCCLACBS', 'CPIAUCSL']:
            for element in data['observations']:
                data[element['date']] = element['value']

        print(data)

if __name__ == '__main__':
    api_call = CallFredAPI(get_api_key())
    api_call.get_historical_data('CPIAUCSL')

