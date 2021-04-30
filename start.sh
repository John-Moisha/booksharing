#!/bin/bash


if [[ "${MODE}" == "runserver" ]]; then
  if [[ "${ENV}" == "dev" ]]; then
    python3 ./app/manage.py runserver 0:8000
  elif [[ "${ENV}" == "prod" ]]; then
    gunicorn booksharing.wsgi --workers=4 --max-requests=10000
  fi
elif [[ "${MODE}" == "worker" ]]; then
  CELERY_PID_FILE="/tmp/celery.pid"
  rm "${CELERY_PID_FILE}"
  celery \
    --app booksharing worker \
    --loglevel=INFO \
    --autoscale=0,20 \
    --pidfile="${CELERY_PID_FILE}"
elif [[ "${MODE}" == "celerybeat" ]]; then
  CELERYBEAT_PID_FILE="/tmp/celerybeat.pid"
  CELERYBEAT_SCHEDULE_FILE="/tmp/celerybeat-schedule"
  rm "${CELERYBEAT_PID_FILE}" "${CELERYBEAT_SCHEDULE_FILE}"
    celery \
  --app booksharing beat \
  --loglevel=INFO \
  --schedule="${CELERYBEAT_SCHEDULE_FILE}" \
  --pidfile="${CELERYBEAT_PID_FILE}"
fi