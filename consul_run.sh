#!/bin/bash

docker run \
    -d \
    -p 8500:8500 \
    -p 8600:8600/udp \
    --name=xxx consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

docker exec xxx consul kv put map_ports "5701 5702 5703"
docker exec xxx consul kv put mq_ports "5701 5702"
docker exec xxx consul kv put mq_name "mq"