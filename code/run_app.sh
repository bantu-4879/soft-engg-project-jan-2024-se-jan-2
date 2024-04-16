#!/bin/bash

#backend 
echo "Activating the virtual environment" 
source venv/bin/activate 
echo "Starting the backend Flask Server" 
cd backend 
export FLASK_APP=app.py
flask run 

#frontend 
echo "Starting the frontend Vue Server" 
cd ../frontend 
npm run serve 



