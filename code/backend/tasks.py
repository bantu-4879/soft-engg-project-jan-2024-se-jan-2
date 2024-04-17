from celery import shared_task
from application.models import Ticket, TicketData
from application.database import db
from application.logger import logger
import joblib 
import os 
import csv

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

@shared_task(bind=True)
def export_ticket_csv_task(self):
    # Fetch all tickets from the database
    tickets = Ticket.query.all()

    if not tickets:
        return {'success': False, 'message': 'No tickets found'}

    csv_filename = 'tickets_report.csv'
    csv_filepath = os.path.join('./databases/csv_files/', csv_filename)

    with open(csv_filepath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ID', 'User ID', 'Title', 'Description', 'Solution', 'Created At', 'Resolved By', 'Solution Satisfaction', 'Ticket Status', 'Ticket Priority', 'Tags List', 'Resolution Time'])

        for ticket in tickets:
            ticket_data = TicketData.query.filter_by(ticket_id=ticket.id).first()
            # Calculate resolution time (assuming resolved_at is a field in your Ticket model)
            resolution_time = None
            if ticket.ticket_status == 'Resolved' and ticket_data.resolved_at:
                resolution_time = ticket_data.resolved_at - ticket.created_at

            csv_writer.writerow([
                ticket.id,
                ticket.user_id,
                ticket.title,
                ticket.description,
                ticket.solution,
                ticket.created_at,
                ticket.resolved_by,
                ticket.solution_satisfaction,
                ticket.ticket_status,
                ticket.ticket_priority,
                ticket.tags_list,
                resolution_time.total_seconds() if resolution_time else None
            ])

    return {'success': True, 'message': 'CSV export completed', 'csv_filename': csv_filename}
     
@shared_task(ignore_result=False)
def test_task(): 
    return "TASK"

def priority_update(): 
    return ""