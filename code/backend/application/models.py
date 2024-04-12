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
    discourse_username=db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "second_name": self.second_name,
            "password": self.password,
            "email": self.email,
            "is_approved": self.is_approved,
            "is_logged": self.is_logged,
            "role_id": self.role_id,
            "card": self.card,
            "profile_photo_loc": self.profile_photo_loc,
            "number_DA": self.number_DA,
            "discourse_username": self.discourse_username
        }

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Authentication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), nullable=True)
    token_created = db.Column(db.Integer,default=0, nullable=True)
    token_expired = db.Column(db.Integer, nullable=True,default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id" : self.user_id, 
            "token" : self.token, 
            "token_created": self.token_created, 
            "token_expired": self.token_expired
        }

class Ticket(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'),nullable=False)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(3000),nullable=False)
    solution = db.Column(db.String(2000))
    thread_link = db.Column(db.String(500))
    privacy=db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.String,nullable=False)
    #date_posted = db.Column(db.Date)
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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "solution": self.solution,
            "thread_link": self.thread_link,
            "privacy": self.privacy,
            "created_at": self.created_at,
            "resolved_by": self.resolved_by,
            "solution_satisfaction": self.solution_satisfaction,
            #"comments": self.comments,
            "ticket_status": self.ticket_status,
            "ticket_priority": self.ticket_priority,
            "tags_list": self.tags_list,
            #"votes": self.votes,
            #"assigned_staff": self.assigned_staff,
            #"comments": self.comments,
            #"attachments": self.attachments

        }

class VoteTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(100), db.ForeignKey('ticket.id'),nullable =False)
    voter_id = db.Column(db.String(100), db.ForeignKey('user.id'),nullable =False)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #ticket_id = db.Column(db.String(100), db.ForeignKey('ticket.id')) #connected to ticket 
    tag_name = db.Column(db.String(100)) 
    description = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "tag_name": self.tag_name,
            "description": self.description,

        }


#Following is the relationship table between tickets and tags 
class TicketsTags(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    tag_id=db.Column(db.Integer,db.ForeignKey('tags.id'),nullable=False)
    ticket_id=db.Column(db.String(100),db.ForeignKey('ticket.id'),nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "tag_id": self.tag_id,
            "ticket_id": self.ticket_id,

        }



class TicketComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable=False)
    comment = db.Column(db.String(1000))
    added_at = db.Column(db.String,nullable=False)
    commenter = db.Column(db.String(100), db.ForeignKey('user.id'))
    user_mentions = db.relationship('User',backref='TicketComments',uselist=True)
    reactions = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "comment": self.comment,
            "added_at": self.added_at,
            "commenter": self.commenter,
            "user_mentions": self.user_mentions,
            "reactions": self.reactions

        }

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
    badge_name = db.Column(db.String(100), db.ForeignKey('badge.badge_name') )
    assigned_by = db.Column(db.String(100), db.ForeignKey('user.id'))

    def to_dict(self):
        return{
            "id" : self.id,
            "user_id" : self.user_id, 
            "badge_name" : self.badge_name
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "opened_at": self.opened_at,
            "assigned_at": self.assigned_at,
            "inProgress_at": self.inProgress_at,
            "resolved_at": self.resolved_at,
            "closed_at": self.closed_at,
            "reopened_at": self.reopened_at

        }

class DisciplinaryAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'),nullable=False)
    flagged_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    approved_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    flagged_till = db.Column(db.String(100), nullable=False)
    flagged_users = db.relationship('User', foreign_keys=[user_id],backref='disciplinary_actions')
    flagging_staff = db.relationship('User', foreign_keys=[flagged_by],backref='flagged_actions')
    approving_staff = db.relationship('User', foreign_keys=[approved_by], backref='approved_actions')

class FAQ(db.Model):
    id = db.Column(db.String, primary_key=True)
    question = db.Column(db.String, nullable=False)
    solution = db.Column(db.String, nullable=False)
    tags_list=db.Column(db.String) 
    created_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

class FAQAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faq_id = db.Column(db.String(100), db.ForeignKey('faq.id'))
    attachment_location = db.Column(db.String(200))