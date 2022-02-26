#!/bin/bash

python -m uvicorn facade_service.service:app --reload --port 8080 &
python -m uvicorn logging_service.service:app --reload --port 8081 &
python -m uvicorn messages_service.service:app --reload --port 8082 &