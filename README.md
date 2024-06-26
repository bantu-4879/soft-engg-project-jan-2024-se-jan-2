# IITM-SE-Project
Software Engineering Project - IIT Madras Jan 2024 Term 

### Team 2
- Aman Kankriya 
- Steve Richards
- Ishika Goel
- Sahithi Dhara 
- Muskan Sindhu 
- Akriti Vishwas

# Introduction 

Welcome to Panacea, your resolution center for all type of student queries, issues, and concerns! 

This project was developed as part of the Software Engineering course with the aim of enhancing and enriching a previously built foundational project with add-on features including but not limited to the following. 
- Discourse Integration
- Webhook Additions
- User Inbox
- Ticket Priority Predictions
- Ticket Comments, and Escalation 
- Admin Report Generation

The project is mainly built on Python Flask in the backend and Vue.js in the frontend. 

# Getting Started 
## Setting Up 
Please make sure you are in the /code directory. 
- Creating a Virtual Environment
  ```python
  python -m venv venv
- Activating the Virtual Environment
  ```python
  source venv/bin/activate
  
- Installing the Requirements
  ```python
  pip install -r requirements.txt
Note: requirements.txt is in the /code directory 

## Running the Application 

### Hosting 

All the parts of the project will be running on the localhost. The following are the standard ports. However, depending on the device, the ports may change. 


- Backend : 5000
- Frontend : 8080
- Redis-Server: 6379
- Smpt-MailHog, HTTP : 1025, 8025

### Run Commands 

- Commands to Run the Backend and Frontend
  ```python
  chmod +x run_app.sh
  ./run_app.sh

- Commands to Run the Celery Tasks
  ```python
  chmod +x run_celery.sh
  ./run_celery.sh

# Documentation 
- The project API documentation can be found at the following.

  https://app.swaggerhub.com/apis-docs/sahithid20/SE-PROJECT/1.2.0



