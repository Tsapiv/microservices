import os
import uuid

from fastapi import FastAPI, Request
from logging_service import LoggingMultiClient
from messages_service import MessageMultiClient
from utils.config import load_config

app = FastAPI()
config = load_config(os.getenv("config", "config/default.yaml"))['facade']

messages = MessageMultiClient(config["messages"])
logging = LoggingMultiClient(config["logging"])


@app.get("/facade-service")
async def get_messages():
    log_response = logging.get().text
    message_response = messages.get().text
    return f'{log_response} : {message_response}'


@app.post("/facade-service")
async def post_message(request: Request):
    msg = (await request.body()).decode("utf-8")
    logging.post({str(uuid.uuid4()): msg})
    messages.post(msg)
