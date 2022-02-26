import uuid

from fastapi import FastAPI, Request
from logging_service import LoggingClient
from messages_service import MessageClient

app = FastAPI()

logging = LoggingClient(8081)
messages = MessageClient(8082)


@app.get("/facade-service")
async def get_messages():
    log_response = logging.get().text
    message_response = messages.get().text
    return f'{log_response} : {message_response}'


@app.post("/facade-service")
async def post_message(request: Request):
    msg = (await request.body()).decode("utf-8")
    logging.post({str(uuid.uuid4()): msg})
