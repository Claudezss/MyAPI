#!/bin/bash

exec flower -A flask_app.worker.tasks.celery_app --broker="$CELERY_BROKER_URL" --port=5555
