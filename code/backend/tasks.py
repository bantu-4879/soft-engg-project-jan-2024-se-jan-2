from celery import shared_task
from application.models import Ticket,User,Role,TicketData
from application.database import db
from application.logger import logger
import joblib 
import os 
import csv
import logging
import datetime
from application.views.inbox_bp import post_message
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
            # Calculate resolution time (assuming resolved_at is a field in your Ticket model)
            resolution_time = None
            ticket_data=TicketData.query.filter_by(ticket_id=ticket.id).first()
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
     
@shared_task
def send_monthly_ticket_report():
    # Fetch users with the 'user' role
    users = User.query.filter_by(role_id = 3).all()
    # Get current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Calculate previous month and year
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    # Fetch tickets resolved by staff users and created by students
    staff=User.query.filter_by(role_id=2)
    for staff_i in staff:
     count=0
     tickets_resolved_by_staff = Ticket.query.filter(Ticket.ticket_status == 'Resolved').filter(resolved_by=staff_i.id).all()
     for ticket in tickets_resolved_by_staff:
          if ticket.created_at.month == previous_month and ticket.created_at.year == previous_year:
               count=count+1
          post_message(staff.id,f"You have resolved {count} ticket/s on Ticket Resolution App in the month of {previous_month}/{previous_year}.","inbox")
     
     for user in users:
         count=0
         resolved_tickets_created_by_user=Ticket.query.filter(Ticket.ticket_status == 'Resolved').filter(user_id=user.id).all()
         for ticket in resolved_tickets_created_by_user:
          if ticket.created_at.month == previous_month and ticket.created_at.year == previous_year:
               count=count+1 
          post_message(user.id,f"The ticket has resolved  {count} ticket/s for you in the month of {previous_month}/{previous_year}.","inbox")
          
     
    # Send monthly report to each user
    
     logging.info("Monthly ticket report inbox message sent.")


@shared_task(ignore_result=False)
def test_task(): 
    return "TASK"

def priority_update(): 
    return ""