import sys
import uuid
from argparse import ArgumentParser

import uvicorn
from consul import Consul
from fastapi import FastAPI, Request

sys.path.append('.')
from logging_service.multi_client import LoggingMultiClient
from messages_service.multi_client import MessageMultiClient
from utils.config import get_ports

app = FastAPI()

parser = ArgumentParser()
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
iid = f'facade{args.port}'

consul = Consul()
consul.agent.service.register(name=iid, port=args.port)
mq_ports = consul.kv.get('mq_ports')[1]['Value'].decode("utf-8").split()
mq_name = consul.kv.get('mq_name')[1]['Value'].decode("utf-8")
ports = get_ports(consul)

messages = MessageMultiClient(ports["messages"], mq_ports, mq_name)
logging = LoggingMultiClient(ports["logging"])


@app.get("/facade-service")
async def get_messages():
    ports = get_ports(consul)
    messages.update(ports['messages'])
    logging.update(ports['logging'])
    log_response = logging.get().text
    message_response = messages.get().text
    return f'{log_response} : {message_response}'


@app.post("/facade-service")
async def post_message(request: Request):
    msg = (await request.body()).decode("utf-8")
    ports = get_ports(consul)
    messages.update(ports['messages'])
    logging.update(ports['logging'])
    logging.post({str(uuid.uuid4()): msg})
    messages.post(msg)


if __name__ == '__main__':
    uvicorn.run("service:app", port=args.port, reload=True)
