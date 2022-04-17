import os

import hazelcast
from fastapi import FastAPI, Request

hport = os.getenv("hport", "5701")

app = FastAPI()
hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}"], cluster_name="dev")
hash_map = hz.get_map("logging").blocking()


@app.get("/logging")
async def get():
    msg = list(hash_map.values())
    print(msg)
    return msg


@app.post("/logging")
async def post(request: Request):
    msg = await request.json()
    key, value = list(msg.items())[0]
    hash_map.put(key, value)
    print(msg)


@app.on_event("shutdown")
def shutdown_event():
    hz.shutdown()
