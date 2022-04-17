import random
from typing import Dict

from .client import LoggingClient


class LoggingMultiClient:

    def __init__(self, ports=None):
        if ports is None:
            ports = [8080]
        self.clients = [LoggingClient(port) for port in ports]

    def post(self, msg: Dict):
        return random.choice(self.clients).post(msg)

    def get(self):
        return random.choice(self.clients).get()
