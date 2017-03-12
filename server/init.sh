rm /code/server/celerybeat.pid
nohup celery -A server.sentry.sentry beat &
nohup celery -A server.sentry.sentry worker &
python3 server/run.py