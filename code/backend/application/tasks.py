from celery import shared_task
from models import Ticket
import joblib 

'''@client.task
def make_predictions(ticket_id):
    try:

    model=joblib('pre-trained-model.pkl')
'''
#priority update 

@shared_task
def test_task(): 
    return "TASK"


def priority_update(): 
    return ""