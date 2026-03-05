import requests
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
key_path = os.path.join(project_root,"config", "api_config.json")

with open(key_path) as f:
    key = json.load(f)['key']

url = f'https://api.stlouisfed.org/fred/series?series_id=DRCCLACBS&api_key={key}&file_type=json'

response = requests.get(url)

print(response.status_code)