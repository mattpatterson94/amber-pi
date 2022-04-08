from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

amber_api_key = os.getenv('AMBER_API_KEY')

response = requests.get(
  'https://api.amber.com.au/v1/sites',
  headers = {
    "Authorization": f'Bearer {amber_api_key}',
    "accept": "application/json"
  }
)
sites = json.loads(response.text)

for site in sites:
  print(f'Site:\n  ID: {site["id"]}\n  NMI: {site["nmi"]}\n  Network: {site["network"]}')
