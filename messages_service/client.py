import hazelcast
from httpx import Client


class MessageClient:

    def __init__(self, port=8080, hports=(5701,), mq_name='mq'):
        self.client = Client(base_url=f'http://127.0.0.1:{port}')
        self.hports = hports
        self.mq_name = mq_name
        self.hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}" for hport in hports], cluster_name="dev")
        self.queue = self.hz.get_queue(mq_name)

    def __del__(self):
        self.hz.shutdown()

    def get(self):
        return self.client.get('/messages')

    def post(self, msg):
        self.queue.put(msg)
