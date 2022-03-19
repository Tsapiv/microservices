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
    map = hz.get_map("map").blocking()
    # Standard Put and Get
    key = '1'
    value = 0
    map.put_if_absent(key, value)
    for k in range(1000):
        if k % 100 == 0:
            print(f"At: {k}")
        while True:
            value = map.get(key)
            if map.replace_if_same(key, value, value + 1):
                break
    print(map.get(key))

    # Shutdown this Hazelcast Client
    hz.shutdown()
