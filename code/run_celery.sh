#!/bin/bash

echo "Activating Virtual Environment"
source venv/bin/activate
cd backend
echo "Starting Redis Server..." 
redis-server 

echo "Starting Celery Worker..."
celery -A app:celery_app worker --loglevel=INFO --pool=solo 
celery -A app:celery_app beat --loglevel=INFO
