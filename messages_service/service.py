from fastapi import FastAPI

app = FastAPI()


@app.get("/messages")
async def get():
    return 'not implemented yet'

