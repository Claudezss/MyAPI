#!/bin/bash

exec celery worker -A flask_app.worker.tasks.celery_app --broker="$CELERY_BROKER_URL"\
 --loglevel=info --autoscale=5,1
