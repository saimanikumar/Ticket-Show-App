#!/bin/bash

# Create a virtual environment and activate it
cd backend

virtualenv env
source env/bin/activate


# Open a new terminal window and start the Redis server
redis-server

# 
celery -A main.celery worker -l info

# 
celery -A main.celery beat --max-interval 1 -l info

#
/home/y20cs045/go/bin/MailHog

mailhog \
-api-bind-addr 127.0.0.1:8025 \
-ui-bind-addr 127.0.0.1:8025 \
-smtp-bin-addr 127.0.0.1.1025