import requests
import json
import os
import psycopg


def get_api_key():
    """
    This retrieves the api key from the project directory needed for a particular API
    """
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
        """
        This gets the historical data for a specific economic series from the FRED website
        """
        self.set_series(series)
        self.set_url()

        response = requests.get(self.url)
        if response.status_code == 200:
            data = [self.series]
            parsed_json = self.parse_json_data(response.json())
            data.append(parsed_json)
            return data
        else:
            print(response.status_code)

    def parse_json_data(self, data):
        """
        This takes the data from the response from the FRED api call and parses the JSON to get the relevant information
        """
        parsed_data = {}
        if self.series in ['DRCCLACBS', 'CPIAUCSL', 'UNRATE', 'MORTGAGE30US', 'TOTALSL']:
            for element in data['observations']:
                parsed_data[element['date']] = element['value']

        return parsed_data

def load_data_to_sql(table, data):
    with psycopg.connect("user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT column_name FROM information.schema.columns WHERE table_name = {table}")


if __name__ == '__main__':
    api_call = CallFredAPI(get_api_key())
    print(api_call.get_historical_data('DRCCLACBS'))
    print(load_data_to_sql("consumer_lending_risk", 0))

