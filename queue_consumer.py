import hazelcast
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', type=str, default='5701')


args = parser.parse_args()

if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient(
        cluster_members=[
            f"localhost:{args.port}",
        ],
        cluster_name="dev",
    )
    queue = hz.get_queue("queue").blocking()
    # Standard Put and Get

    for _ in range(100):
        k = queue.take()
        print(f'{k} has been taken by localhost:{args.port}')

    # Shutdown this Hazelcast Client
    hz.shutdown()
