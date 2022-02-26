from typing import Dict
from httpx import Client, Response


class LoggingClient:

    def __init__(self, port=8080):
        self.client = Client(base_url=f'http://127.0.0.1:{port}')

    def post(self, msg: Dict):
        return self.client.post('/logging', json=msg)

    def get(self):
        return self.client.get('/logging')
