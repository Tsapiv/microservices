from typing import Dict

from httpx import Client


class MessageClient:

    def __init__(self, port=8080):
        self.client = Client(base_url=f'http://127.0.0.1:{port}')

    def get(self):
        return self.client.get('/messages')
