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
        value = map.get(key)
        # sleep(10)
        value += 1
        map.put(key, value)
    print(map.get(key))

    # Shutdown this Hazelcast Client
    hz.shutdown()
