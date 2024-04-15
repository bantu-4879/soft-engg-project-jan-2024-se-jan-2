from celery import shared_task
from application.models import Ticket
from application.database import db
from application.logger import logger
import joblib 

# @shared_task(ignore_result=False)
# def make_predictions(ticket_id):
#     try:
#         ticket = Ticket.query.filter_by(id=ticket_id).first() 
#         loaded_model = joblib.load('pre-trained-model.pkl')
#         predicted_priority = loaded_model.predict(ticket.description)
#         ticket.priority = predicted_priority 
#         db.session.commit() 
#         return predicted_priority
#     except Exception as e:
#         logger.error(f"Exception from make_predictions {e}")


#priority update 

@shared_task(ignore_result=False)
def test_task(): 
    return "TASK"

def priority_update(): 
    return ""