from argparse import ArgumentParser

import hazelcast
import uvicorn as uvicorn
from consul import Consul
from fastapi import FastAPI, Request

app = FastAPI()
parser = ArgumentParser()
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
iid = f'logging{args.port}'

consul = Consul()
consul.agent.service.register(name=iid, port=args.port)

hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}" for
                                                hport in consul.kv.get('map_ports')[1]['Value'].decode("utf-8").split()],
                               cluster_name="dev")
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
    consul.agent.service.deregister(iid)


if __name__ == '__main__':
    uvicorn.run("service:app", port=args.port, reload=True)
