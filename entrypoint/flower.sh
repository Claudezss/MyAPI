#!/bin/bash

exec flower -A flask_app.worker.tasks.celery_app --broker=amqp://admin:mypass@rabbit:5672 --port=5555
