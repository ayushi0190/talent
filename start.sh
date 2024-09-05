#!/bin/bash
echo "Running start.sh"
echo "Running celery..."
celery -A src.utilities.tasks worker --loglevel=INFO -B &
service ssh start
echo "Running fastapi"
#python3 -m src.routes.main
# gunicorn src.routes.main:app --bind 0.0.0.0:9003 --workers 2 --threads 2 --worker-connections 1024 --backlog 256 -k uvicorn.workers.UvicornWorker --max-requests 1000 --max-requests-jitter 30 --timeout 30
uvicorn src.routes.main:app --host 0.0.0.0 --port 9003
