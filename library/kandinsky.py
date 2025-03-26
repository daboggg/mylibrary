import json
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("KANDINSKY_API_KEY")
SECRET_KEY = os.getenv("KANDINSKY_SECRET_KEY")

log = logging.getLogger(__name__)


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=768, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()

        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)

def get_image_from_kandinsky(prompt:str):
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    pipeline_id = api.get_pipeline()
    log.info(time.ctime())
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)

    log.info(time.ctime())
    return files[0]
