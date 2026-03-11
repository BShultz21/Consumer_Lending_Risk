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
        self.url = f'https://api.stlouisfed.org/fred/series/observations?series_id={self.series}&observation_start=1991-01-01&api_key={self.key}&file_type=json'

    def set_series(self, series):
        self.series = series

    def set_url(self):
        self.url = f'https://api.stlouisfed.org/fred/series/observations?series_id={self.series}&observation_start=1991-01-01&api_key={self.key}&file_type=json'

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
        if self.series in ['DRCCLACBS', 'CPIAUCSL', 'UNRATE', 'MORTGAGE30US', 'TOTALSL', 'TDSP']:
            for element in data['observations']:
                parsed_data[element['date'] ] = element['value']
        print(parsed_data)
        return parsed_data

def load_to_sql(table, data):
    with psycopg.connect("user=postgres") as conn:
        with conn.cursor() as cur:
            rows = []
            indicator = data[0]
            for date, value in data[1].items():
                if value in ('', '.', 'N/A', None):
                    value = None
                rows.append((date, value, indicator))

            cur.executemany(
                f'INSERT INTO {table} (date, value, indicator_id) VALUES (%s, %s, %s)',
                rows
            )

    print("Data has been loaded")


def load_historical_data():
    """
    This calls the API to get historical data, parses the data, and then loads to SQL
    """

    api_call = CallFredAPI(get_api_key())
    metrics = ['DRCCLACBS', 'CPIAUCSL', 'UNRATE', 'MORTGAGE30US', 'TOTALSL', 'TDSP']
    for metric in metrics:
        data = api_call.get_historical_data(metric)
        load_to_sql("consumer_lending_risk", data)


if __name__ == '__main__':
    load_historical_data()
