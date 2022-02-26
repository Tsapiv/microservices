from multiprocessing import Manager
from fastapi import FastAPI, Request

app = FastAPI()
manager = Manager()
hash_map = manager.dict()


@app.get("/logging")
async def get():
    return list(hash_map.values())


@app.post("/logging")
async def post(request: Request):
    msg = await request.json()
    hash_map.update(msg)
    print(msg)
