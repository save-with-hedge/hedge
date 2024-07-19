#!/bin/bash

NAME=hedge
DIR=/home/hedge-nico/hedge
USER=hedge-nico
GROUP=hedge-nico
WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker
VENV=$DIR/.venv/bin/activate
#BIND=unix:$DIR/run/gunicorn.sock
PORT=8000
LOG_LEVEL=info

cd $DIR
source $VENV

exec gunicorn app:app \
  --name $NAME \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --user=$USER \
  --group=$GROUP \
  --bind 0.0.0.0:$PORT \
  --log-level=$LOG_LEVEL \
  --log-file=-
