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

    for k in range(100):
        queue.put(k)
        print(f'{k} is in the queue; try to put {k + 1}')

    # Shutdown this Hazelcast Client
    hz.shutdown()
