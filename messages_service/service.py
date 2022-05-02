import os
import threading
from datetime import datetime

import hazelcast
from fastapi import FastAPI

from utils.config import load_config

app = FastAPI()

hport = os.getenv("hport", "5701")
config = load_config(os.getenv("config", "config/default.yaml"))['messages']

hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}"], cluster_name="dev")
queue = hz.get_queue(config['mq_name']).blocking()
filename = os.path.join(config['msg_dir'], f"{datetime.now().isoformat()}.txt")


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
