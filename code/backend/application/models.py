#this is for db models
from application.database import db
import datetime


#The following table has relationship (many- many) between tickets and the staff assigned
assigned_staff_tickets = db.Table('assigned_staff_tickets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'))
)
class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    #auth = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean,default=False, nullable=False)
    is_logged = db.Column(db.Boolean, default=False, nullable=False)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    card = db.Column(db.String(100), nullable=False,default="Green")
    profile_photo_loc = db.Column(db.String, default="", nullable=True)
    number_DA = db.Column(db.Integer) #number of disciplinary actions taken for user
    authentication = db.relationship('Authentication', backref='user', uselist=False) #to check for tokens
    #disciplinary_actions = db.relationship('DisciplinaryAction', foreign_keys='DisciplinaryAction.user_id',backref='user_associated', lazy='dynamic') # relationship with disciplinary actions.
    #flagging_actions = db.relationship('DisciplinaryAction',foreign_keys='DisciplinaryAction.flagged_by', backref='flagged_by_user', lazy='dynamic')
    #approving_actions = db.relationship('DisciplinaryAction',  foreign_keys='DisciplinaryAction.approved_by',backref='approved_by_user', lazy='dynamic')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Authentication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), nullable=True)
    token_created = db.Column(db.Integer,default=0, nullable=True)
    token_expired = db.Column(db.Integer, nullable=True,default=0)

class Ticket(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'),nullable=False)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(3000),nullable=False)
    solution = db.Column(db.String(2000))
    thread_link = db.Column(db.String(500))
    privacy=db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.String,nullable=False)
    resolved_by = db.Column(db.String(100), db.ForeignKey('user.id'),default=0,nullable=False)
    solution_satisfaction = db.Column(db.Boolean,nullable=False) 
    comments = db.Column(db.String(500))
    ticket_status=db.Column(db.String(100),nullable=False)
    ticket_priority = db.Column(db.Float)
    tags_list=db.Column(db.String)  #list of tags 
    #tags = db.relationship('TicketTags',backref='tickets',lazy=True) #tags related to the ticket - many - many relationship
    votes = db.relationship('VoteTable', backref='ticket',uselist=True) #The votes and who votes one - many relationship
    assigned_staff = db.relationship('User', secondary=assigned_staff_tickets,
                                     backref='assigned_tickets', lazy='dynamic') #many to many relationship assigned staff
    comments=db.relationship('TicketComments', backref='ticket',uselist=True) #the comments made by staff to the ticket one - many relationship
    attachments=db.relationship('TicketAttachment', backref='ticket',uselist=True) #ticket attachments one - many relationship (we can limit to 2)

class VoteTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(100), db.ForeignKey('ticket.id'),nullable =False)
    voter_id = db.Column(db.String(100), db.ForeignKey('user.id'),nullable =False)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #ticket_id = db.Column(db.String(100), db.ForeignKey('ticket.id')) #connected to ticket 
    tag_name = db.Column(db.String(100)) 
    description = db.Column(db.String(200))


#Following is the relationship table between tickets and tags 
class Tickets_Tags(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    tag_id=db.Column(db.Integer,db.ForeignKey('tag.id'),nullable=False),
    ticket_id=db.Column(db.String(100),db.ForeignKey('ticket.id'),nullable=False)


class TicketComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable=False)
    comment = db.Column(db.String(1000))
    added_at = db.Column(db.String,nullable=False)
    commenter = db.Column(db.String(100), db.ForeignKey('user.id'))
    user_mentions = db.relationship('User',backref='TicketComments',uselist=True)
    reactions = db.Column(db.String(100))

class TicketAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(100), db.ForeignKey('ticket.id'))
    attachment_location = db.Column(db.String(200))


class Inbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    message = db.Column(db.String)
    received_at = db.Column(db.String,nullable=False)
    have_read = db.Column(db.Boolean)
    message_type = db.Column(db.String(100),nullable=False)

class AssignBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    badge_name = db.Column(db.Integer, db.ForeignKey('badge.badge_name') )
    assigned_by = db.Column(db.String(100), db.ForeignKey('user.id'))

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_name=db.Column(db.String(100), nullable=False, unique=True) 
    badge_picture_location = db.Column(db.String(200), nullable=False)

class TicketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(100), db.ForeignKey('ticket.id'),nullable=False)
    opened_at=db.Column(db.String)
    assigned_at=db.Column(db.String)
    inProgress_at=db.Column(db.String)
    resolved_at = db.Column(db.String)
    closed_at= db.Column(db.String)
    reopened_at=db.Column(db.String)

class DisciplinaryAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'),nullable=False)
    flagged_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    approved_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    flagged_till = db.Column(db.String(100), nullable=False)
    flagged_users = db.relationship('User', foreign_keys=[user_id],backref='disciplinary_actions')
    flagging_staff = db.relationship('User', foreign_keys=[flagged_by],backref='flagged_actions')
    approving_staff = db.relationship('User', foreign_keys=[approved_by], backref='approved_actions')
    