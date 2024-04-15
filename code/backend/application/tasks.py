from celery import Celery 
from models import Ticket
import joblib 

'''@client.task
def make_predictions(ticket_id):
    try:

    model=joblib('pre-trained-model.pkl')
'''
#priority update 

def priority_update(): 
    return ""