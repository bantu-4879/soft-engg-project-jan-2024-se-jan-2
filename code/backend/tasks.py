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

@shared_task
def create_report():
    print("yugdgf")
    '''
     if not theater:
          return {'success':False,'message':'Theater does not exist'}
     csv_filename=f'theater_{theater_id}_report.csv'
     csv_filepath = os.path.join('./csv_files/', csv_filename) 
     with open(csv_filepath,'w',newline='') as csvfile:
          csv_writer=csv.writer(csvfile)
          csv_writer.writerow(['Show Name','Number of Bookings','Average Rating','Viewer Comments','Genre','Ticket Price','Revenue','Show Timings','Date','Duration (mins)'])
          shows=theater.shows
          for show in shows:
               bookings=db.session.query(func.coalesce(db.func.sum(Booking.num_tickets),0)).filter(Booking.show_id==show.show_id).scalar()
               average_rating=db.session.query(func.avg(Review.rating)).filter_by(show_id=show.show_id).scalar()
               show_rating=show.rating
               if(average_rating):
                    show_rating=average_rating
               comments=[]
               reviews=Review.query.filter_by(show_id=show.show_id).all()
               for review in reviews:
                    comments.append(review.comment)
               revenue=show.ticket_price*bookings
               time1=show.time.strftime("%I:%M %p")
               date=show.Date_start.strftime('%d/%m/%Y')
               csv_writer.writerow([show.name, bookings, show_rating, comments, show.genre, show.ticket_price, revenue, time1, date,show.time_interval])
     return {'success':True,'message':'CSV export completed','csv_filename':csv_filename}'''
     
@shared_task(ignore_result=False)
def test_task(): 
    return "TASK"

def priority_update(): 
    return ""