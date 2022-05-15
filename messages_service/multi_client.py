import random
from typing import Dict

from .client import MessageClient


class MessageMultiClient:

    def __init__(self, ports, hports, mq_name):
        self.ports = ports
        self.hports = hports
        self.mq_name = mq_name
        self.clients = [MessageClient(port, hports, mq_name) for port in ports]

    def update(self, ports):
        remove = set(self.ports) - set(ports)
        add = set(ports) - set(self.ports)
        for port in remove:
            idx = self.ports.index(port)
            del self.ports[idx]
            del self.clients[idx]
        for port in add:
            self.clients.append(MessageClient(port, self.hports, self.mq_name))
            self.ports.append(port)

    def post(self, msg: Dict):
        return random.choice(self.clients).post(msg)

    def get(self):
        return random.choice(self.clients).get()
