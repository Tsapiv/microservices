import os
import threading
from argparse import ArgumentParser
from datetime import datetime

import hazelcast
import uvicorn
from consul import Consul
from fastapi import FastAPI

app = FastAPI()
parser = ArgumentParser()
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
iid = f'messages{args.port}'

consul = Consul()
consul.agent.service.register(name=iid, port=args.port)

hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}" for
                                                hport in consul.kv.get('mq_ports')[1]['Value'].decode("utf-8").split()],
                               cluster_name="dev")

queue = hz.get_queue(consul.kv.get('mq_name')[1]['Value'].decode("utf-8")).blocking()
filename = os.path.join("data", f"{datetime.now().isoformat()}.txt")


def save_msg():
    while True:
        msg = queue.take()
        print(f"INFO:\tMQ receive: {msg}")
        with open(filename, 'a') as f:
            f.write(f"{msg}\n")


@app.on_event('startup')
async def app_startup():
    threading.Thread(target=save_msg, daemon=True).start()


@app.get("/messages")
async def get():
    with open(filename, 'r') as f:
        return list(map(lambda x: x.strip(), f.readlines()))


@app.on_event("shutdown")
def shutdown_event():
    hz.shutdown()


if __name__ == '__main__':
    uvicorn.run("service:app", port=args.port, reload=True)
