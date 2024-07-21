WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker
PORT=8000
LOG_FILE=logs/gunicorn.log

exec gunicorn hedge:app \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --bind 0.0.0.0:$PORT \
