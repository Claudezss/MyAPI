#!/bin/bash

echo "Starting Flask App"
exec gunicorn --workers "${PROCESS_COUNT:-2}" --threads "${THREAD_COUNT:-2}"\
 --timeout 600 --bind 0.0.0.0:8000 flask_app.wsgi:app