#!/bin/bash
# print our ip address
#ip -br addr show up scope global

set -ex

echo "Starting Django application..."

# cd /app
python3 manage.py migrate --noinput


echo "Starting Gunicorn server..."
# exec "$@"

exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3
echo "AELZ Django demo entrypoint completed"
