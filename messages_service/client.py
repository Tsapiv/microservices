import hazelcast
from httpx import Client


class MessageClient:

    def __init__(self, port=8080, hport=5701):
        self.client = Client(base_url=f'http://127.0.0.1:{port}')
        self.hz = hazelcast.HazelcastClient(
            cluster_members=[
                f"localhost:{hport}",
            ],
            cluster_name="dev",
        )
        self.queue = self.hz.get_queue("mq")

    def get(self):
        return self.client.get('/messages')

    def post(self, msg):
        self.queue.put(msg)

