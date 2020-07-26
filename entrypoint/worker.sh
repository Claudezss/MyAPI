#!/bin/bash

exec celery worker -A flask_app.worker.tasks.celery_app --broker=amqp://admin:mypass@rabbit:5672\
 --loglevel=info --autoscale=5,1