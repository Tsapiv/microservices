

import hazelcast

if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient(
        cluster_members=[
            "localhost:5701",
            "localhost:5702",
            "localhost:5703"
        ],
        cluster_name="dev",
    )
    # Get the Distributed Map from Cluster.
    map = hz.get_map("my-distributed-map").blocking()
    # Standard Put and Get
    for idx in range(1000):
        map.put(f"key_{idx}", idx)
    print(map.get("key_999"))

    # Shutdown this Hazelcast Client
    hz.shutdown()


