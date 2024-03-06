#this is for db models
from application.database import db
import datetime
# UserMixin for common user attributes and methods

assigned_staff_tickets = db.Table('assigned_staff_tickets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'))
)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    auth = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    card = db.Column(db.String(100), nullable=False)
    authentication = db.relationship('Authentication', backref='user', uselist=False)
    disciplinary_actions = db.relationship('DisciplinaryAction', backref='user', uselist=True)
    assigned_tickets = db.relationship('Ticket', secondary=assigned_staff_tickets,
                                       backref=db.backref('assigned_staff', lazy='dynamic'))

# RoleMixin for common role attributes
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


class Authentication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    token_created = db.Column(db.String(100), nullable=False)
    token_expired = db.Column(db.String(100), nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(3000),nullable=False)
    solution = db.Column(db.String(2000))
    thread_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    resolved_at = db.Column(db.DateTime)
    solution_satisfaction = db.Column(db.Boolean,nullable=False)
    comments = db.Column(db.String(500))
    ticket_status=db.Column(db.String(100),nullable=False)
    ticket_priority = db.Column(db.Float)
    tags = db.relationship('Ticket_Tags',secondary='tickets_tags',backref='tickets')
    votes = db.relationship('VoteTable', backref='ticket',uselist=True)
    assigned_staff = db.relationship('User', secondary=assigned_staff_tickets,
                                     backref=db.backref('assigned_tickets', lazy='dynamic'))
    comments=db.relationship('TicketComments', backref='ticket',uselist=True)
    attachments=db.relationship('TicketAttachment', backref='ticket',uselist=True)

class VoteTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable =False)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable =False)

class TicketTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    tags = db.Column(db.String(100))
    name = db.Column(db.String(100))

tickets_tags=db.Table('tickets_tags',
    db.Column('ticket_id',db.Integer,db.ForeignKey('ticket.id')),
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'))
)

class TicketComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable=False)
    comment = db.Column(db.String(1000))
    added_at = db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    commenter = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_mentions = db.relationship('User',backref='TicketComments',uselist=True)
    reactions = db.Column(db.String(100))

class TicketAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    attachment_location = db.Column(db.String(200))


class Inbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(500),nullable=False)
    received_at = db.Column(db.DateTime,nullable=False)
    have_read = db.Column(db.Boolean)
    message_type = db.Column(db.String(100),nullable=False)

class StaffBadges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    badge_name=db.Column(db.String(100), nullable=False)
    badge_picture_location = db.Column(db.String(200))
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class TicketData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    opened_at=db.Column(db.DateTime)
    assigned_at=db.Column(db.DateTime)
    inProgress_at=db.Column(db.DateTime)
    reopened_at=db.Column(db.DateTime)

class DisciplinaryAction(db.Model):
    disciplinary_action_id = db.Column(db.Integer, db.ForeignKey('disciplinary_action.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    flagged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flagged_till = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)