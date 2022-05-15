import random
from typing import Dict

from .client import LoggingClient


class LoggingMultiClient:

    def __init__(self, ports: list):
        self.ports = ports
        self.clients = [LoggingClient(port) for port in ports]

    def update(self, ports):
        remove = set(self.ports) - set(ports)
        add = set(ports) - set(self.ports)
        for port in remove:
            idx = self.ports.index(port)
            del self.ports[idx]
            del self.clients[idx]
        for port in add:
            self.clients.append(LoggingClient(port))
            self.ports.append(port)

    def post(self, msg: Dict):
        return random.choice(self.clients).post(msg)

    def get(self):
        return random.choice(self.clients).get()
