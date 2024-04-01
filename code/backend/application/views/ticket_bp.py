# - get specific ticket *
# - post a new ticket *  # add the details to the ticket_tags 
# - update a ticket *
# - delete a ticket *
# - vote a ticket  *



# - solving a ticket & 
# - assigning a ticket & 
# - get tickets by assigned tickets &

# - get comments of a ticket % 
# - post comment &
# - edit comment &
# - delete comment &

# --------------------  Imports  --------------------

from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
import hashlib
import time
from application.database import db
from application.common_utils import (
    token_required,
    users_required,
)
from application.common_utils import (
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from application.views.user_utils import UserUtils,time_to_str
from application.responses import *
from application.globals import *
from application.models import *
from copy import deepcopy
from application.notifications import send_email

# --------------------  Code  --------------------

# -- Ticket Utils -- 

class TicketUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id=user_id
    
    def convert_ticket_to_dict(self, ticket):
        ticket_dict = vars(ticket)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in ticket_dict:
            del ticket_dict["_sa_instance_state"]
        attachments = self.get_ticket_attachments(ticket_id=ticket.id)
        ticket_dict["attachments"] = attachments
        return ticket_dict
    
    def get_ticket_attachments(self,ticket_id):
        ticket_attch = TicketAttachment.query.filter_by(ticket_id=ticket_id).all()
        attachments = []
        for att in ticket_attch:
            file_path = att.attachment_loc
            img_base64 = ""
            if is_img_path_valid(file_path):
                img_base64 = convert_img_to_base64(file_path)
            d_ = {"ticket_id": att.ticket_id, "attachment_loc": img_base64}
            attachments.append(d_)
        return attachments
    
    def generate_ticket_id(self, title: str, user_id: str) -> str:
        """
        Ticket id is generated from ticket title and ticket id and timestamp
        """
        # generate unique id
        ts = str(int(time.time_ns()))
        string = f"{user_id}_{title}_{ts}"
        ticket_id = hashlib.md5(string.encode()).hexdigest()
        return ticket_id

    def save_ticket_attachments(
        self, attachments: list, ticket_id: str, user_id: str, operation: str
    ):
        # get list of files from db for the ticket and user
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {ticket_id}_{user_id}_{number-extension-if-needed}_.{file_format}
        # operation : create_ticket , update_ticket only student can do | resolve_ticket only support can do.

        total_attachments = len(attachments)
        num_successful_attachments = 0

        if total_attachments == 0:
            return (False, "Attachments are empty.")

        files = [
            file
            for file in os.listdir(TICKET_ATTACHMENTS_PATH)
            if file.startswith(f"{ticket_id}_{user_id}")
        ]
        number_extension = len(files)  # starting point

        for attach in attachments:
            # attach will be of format {attachment_loc:'', user_id:''}
            # attachment_loc will contain base64 version of image while data transfer is occuring between backend and frontend
            # attachment_loc will contain image path when data is retried from db by backend
            # attachment_loc will contain base64 image when creating new attachment

            if attach["attachment_loc"]:
                if is_base64(attach["attachment_loc"].split(",")[1]):
                    file_type, file_format, encoded_data = get_encoded_file_details(
                        attach["attachment_loc"]
                    )
                    if (file_type == "image") and (
                        file_format in ACCEPTED_IMAGE_EXTENSIONS
                    ):
                        file_name = (
                            f"{ticket_id}_{user_id}_{number_extension}.{file_format}"
                        )
                        file_path = os.path.join(TICKET_ATTACHMENTS_PATH, file_name)
                        if convert_base64_to_img(file_path, encoded_data):
                            # successfully image saved and now add entry to database
                            try:
                                # while creating a ticket a student can upload multiple attachments
                                # verify whether each attachment is unique
                                attach["ticket_id"] = ticket_id
                                attach["attachment_loc"] = file_path
                                ticket_attach = TicketAttachment(
                                    ticket_id=attach["ticket_id"],
                                    attachment_location=attach["attachment_loc"]
                                )
                                db.session.add(ticket_attach)
                                db.session.commit()
                                num_successful_attachments += 1
                                number_extension += 1
                            except Exception as e:
                                logger.error(
                                    f"TicketAPI->post : Error occured while creating a Ticket Attachment : {e}"
                                )
        return (
            True,
            f"Total {num_successful_attachments} / {total_attachments} attchements are valid and added successfully.",
        )
    
    def tickets_filter_by_query(self, all_tickets, query=""):
        # match tickets with query
        filtered_tickets = []
        if query:
            for ticket in all_tickets:
                search_in = (
                    f"{ticket['title']} {ticket['description']} {ticket['solution']}"
                )
                for q in query.split(" "):
                    if q.lower() in search_in.lower():
                        filtered_tickets.append(ticket)
                        break

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_tags(self, all_tickets, tags):
        # filter by tags (if present)
        filtered_tickets = []
        if tags:
            for ticket in all_tickets:
                ticket_tags = ticket["tags"].split(',') #converts tags list into a list
                if set(ticket_tags).intersection(set(tags)):
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_status(self, all_tickets, status=[]):
        # filter by status (if present)
        filtered_tickets = []
        if status:
            for ticket in all_tickets:
                if ticket["ticket_status"] in status:
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_priority(self, all_tickets, priority=[]):
        # filter by priority (if present)
        filtered_tickets = []
        if priority:
            for ticket in all_tickets:
                if ticket["ticket_priority"] in priority:
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_sort(self, all_tickets, sortby="", sortdir=""):
        # sort (if present)
        if sortby:
            # sortby should be 'created_on', 'resolved_on', 'votes'
            if sortby not in ["created_at", "resolved_on", "votes"]:
                sortby = "created_at"
        else:
            sortby = "created_at"
        if sortdir:
            # sortdir should be 'asc' or 'desc'
            sortdir = True if sortdir == "desc" else False
        else:
            sortdir = True
        all_tickets = sorted(all_tickets, key=lambda d: d[sortby], reverse=sortdir)
        return all_tickets

    def tickets_filter_sort(self, all_tickets, args):
        # match tickets with query
        all_tickets = self.tickets_filter_by_query(all_tickets, args["query"])

        # filter by tags (if present)
        all_tickets = self.tickets_filter_by_tags(all_tickets, args["tags"])

        # filter by status (if present)
        all_tickets = self.tickets_filter_by_status(all_tickets, args["status"])

        # filter by priority (if present)
        all_tickets = self.tickets_filter_by_priority(all_tickets, args["priority"])

        # sort (if present)
        all_tickets = self.tickets_sort(all_tickets, args["sortby"], args["sortdir"])

        return all_tickets

    def get_args_from_query(self, args):
        def convert_arg_to_list(arg: str):
            # for internal use only
            arg = args.get(arg, "")
            if arg == "":
                return []
            else:
                return arg.split(",")

        _args = {}
        _args["query"] = args.get("query", "")
        _args["sortby"] = args.get("sortby", "")
        _args["sortdir"] = args.get("sortdir", "")
        _args["status"] = convert_arg_to_list("filter_status")
        _args["priority"] = convert_arg_to_list("filter_priority")
        _args["tags"] = convert_arg_to_list("filter_tags")

        return _args 
    
    def get_voter_list(self,ticket):
        #print("This is a function to return who all voted for the ticket")
        ticket_id=ticket["ticket_id"]
        ticket=Ticket.query.filter_by(id=ticket_id).first()
        voter_list=[]
        for vote in ticket.votes:
            voter_list.append(vote.voter_id)
        return voter_list
    

    def get_ticket_comments(self,comments):
        ticket_comments = vars(comments)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in ticket_comments:
            del ticket_comments["_sa_instance_state"]
        return ticket_comments
    
    def get_ticket_data(self,ticket_id):
        ticket_data=TicketData.query.filter_by(ticket_id=ticket_id).all()
        ticket_data_list=[]
        for each_data in ticket_data:
            ticket_data_list.append(each_data)
        return ticket_data_list
    


ticket_bp = Blueprint("ticket_bp", __name__)
ticket_api = Api(ticket_bp)
ticket_utils = TicketUtils()

class TicketAPI(Resource):
    @token_required
    @users_required(users=["Student", "Staff", "Admin"])
    def get(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Get a single ticket for the user and return

        Parameters
        ----------
        ticket is and user id

        Returns
        -------
        Ticket

        """

        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = User.query.filter_by(id=user_id).first()
                if user_id == ticket.user_id or user.role == "Staff":
                    # the ticket and its user are matched or its a support staff
                    # convert to list of dict
                    ticket_dict = ticket_utils.convert_ticket_to_dict(ticket)
                    return success_200_custom(data=ticket_dict)
            else:
                raise NotFoundError(status_msg="Ticket does not exists")

    @token_required
    @users_required(users=["Student"])
    def post(self, user_id):
        """
        Usage
        -----
        Create a new ticket. Only a student can create.

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "description": "",
            "ticket_priority": "",
            "tag": "",
            "ticket_status":"Open",
            "solution_satisfaction":"False"
        }

        # check user_id
        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is empty/missing in url")

        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                # user id does not exists
                raise NotFoundError(status_msg="User id does not exists.")
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # get form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
            print(details)
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if details["title"] == "" or details["tag"] == "":
                raise BadRequest(
                    status_msg=f"Ticket title and at least one tag is required"
                )

            ticket_id = ticket_utils.generate_ticket_id(details["title"], user_id)
            details["ticket_id"] = ticket_id
            details["created_by"] = user_id
            details["created_on"] = time_to_str(datetime.datetime.now())
            ticket = Ticket(
                id = details["ticket_id"],
                title = details["title"],
                description = details["description"],
                ticket_priority = details["ticket_priority"],
                tags_list = details["tag"],
                ticket_status = "Open",
                solution_satisfaction = False,
                created_at = details["created_on"],
                user_id = details["created_by"]
            )
            ticket_data=TicketData(
                ticket_id=details["ticket_id"],
                opened_at=time_to_str(datetime.datetime.now())
            )

            try:
                db.session.add(ticket)
                db.session.add(ticket_data)
                db.session.commit()
            except Exception as e:
                logger.error(
                    f"TicketAPI->post : Error occured while creating a new ticket : {e}"
                )
                raise InternalServerError(
                    status_msg="Error occured while creating a new ticket"
                )
            else:
                logger.info("Ticket created successfully.")

                # add attachments now
                status, message = ticket_utils.save_ticket_attachments(
                    attachments, ticket_id, user_id, operation="create_ticket"
                )
                raise Success_200(status_msg=f"Ticket created successfully. {message}")

    @token_required
    @users_required(users=["Student", "Staff"])
    def put(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Update a ticket.
        only student and support has access, role is checked later in code.
        Student who created a ticket can update : title, description, attachments, tags, priority
        Student who did not create : can vote a ticket
        Support can update : solution and attachment, status
        update ticket status to inProgress and update ticket data associated

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "description": "",
            "tags": "",
            "priority": "",
            "status": "",
            "votes": 0,
            "solution": "",
            "inProgress":" ",
        }

        
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"TicketAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
            ticket_attachment = TicketAttachment.query.filter_by(
                ticket_id=ticket_id
            ).all()
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching user and ticket data : {e}"
            )
            raise InternalServerError
        else:
            if not ticket:
                raise NotFoundError(status_msg="Ticket does not exists")
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            if ticket.ticket_status == "Resolved":
                raise BadRequest(status_msg=f"Resolved tickets can't be edited.")

            role = user.role.name

            if role == "Staff" or (
                role == "Student" and user_id == ticket.user_id
            ):
                # add attachments now
                status, message = ticket_utils.save_ticket_attachments(
                    attachments, ticket_id, user_id, operation="update_ticket"
                )
                #solution 

            if role == "Student":   #it would be "Student" but for the time being changed it to Admin
                if user_id == ticket.user_id:
                    # student is creator of the ticket
                    if details["title"] == "" or details["tags"] == "":
                        raise BadRequest(
                            status_msg=f"Ticket title and at least one tag is required"
                        )

                    ticket.title = details["title"]
                    ticket.description = details["description"]
                    ticket.tags_list = details["tags"]
                    priority = details["priority"]
                    ticket.ticket_status=details["status"]
                    if(priority=="low"):
                        ticket.ticket_priority=0.15
                    if(priority=="medium"):
                        ticket.ticket_priority=0.50
                    if(priority=="high"):
                        ticket.ticket_priority=0.75
                    db.session.add(ticket)
                    db.session.commit()

                    raise Success_200(status_msg="Successfully updated a ticket.")

                else:
                    # student has not created this ticket, so only vote can be done
                    ticket_vote = VoteTable.query.filter_by(
                        ticket_id=ticket_id, user_id=user_id
                    ).first()
                    if ticket_vote:
                        # student has already voted
                        raise AlreadyExistError(
                            status_msg="You have already voted this ticket."
                        )
                    else:
                        # ticket upvoted
                        ticket_vote = VoteTable(ticket_id=ticket_id, voter_id=user_id)
                        db.session.add(ticket_vote)
                        db.session.commit()
                        raise Success_200(status_msg="Successfully upvoted ticket.")

            if role == "Staff":
                ticket_data=TicketData.query.filter_by(ticket_id=ticket.id).first()

                if(details["inProgress"] == "yes"):
                    ticket_data.inProgress=time_to_str(datetime.datetime.now())
                    db.session.add(ticket_data)
                    db.session.commit()
            
                elif(details["inProgress"]=="no"):
                    sol = details["Solution"]
                    if ticket_utils.is_blank(sol):
                        raise BadRequest(status_msg="Solution can not be empty")
                    else:
                        ticket.solution = sol
                        ticket.ticket_status = "Resolved"
                        ticket.resolved_by = user_id
                        ticket_data.resolved_at = time_to_str(time.time())
                        db.session.add(ticket)
                        db.session.add(ticket_data)
                        db.session.commit()

                    # send notification to user who created as well as voted , separately handled.

            # if role == "Admin":
            #     # admin dont have access
            #     raise Unauthenticated(
            #         status_msg="Admin don't have access to this endpoint."
            #     )

    # @token_required
    # @users_required(users=["Student"])
    def delete(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Delete a single ticket. Only a student who created  a ticket can delete

        Parameters
        ----------
        ticket is and user id

        Returns
        -------


        """
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->delete : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = User.query.filter_by(id=user_id).first()
                if user.id == ticket.user_id:
                    # the ticket and its user are matched

                    # delete ticket votes
                    ticket_votes = VoteTable.query.filter_by(ticket_id=ticket_id).all()
                    for ticket_vote in ticket_votes:
                        db.session.delete(ticket_vote)
                    db.session.commit()

                    # delete ticket attachments
                    ticket_attachments = TicketAttachment.query.filter_by(
                        ticket_id=ticket_id
                    ).all()
                    for ticket_attachment in ticket_attachments:
                        db.session.delete(ticket_attachment)
                    db.session.commit()

                    # delete ticket
                    db.session.delete(ticket)
                    db.session.commit()
                    raise Success_200(status_msg="Ticket deleted successfully")
                else:
                    raise PermissionDenied(
                        status_msg="Only a user who created a ticket can delete it."
                    )
            else:
                raise NotFoundError(status_msg="Ticket does not exists")


class AllTicketsAPI(Resource):
    @token_required
    @users_required(users=["Student", "Staff", "Admin"])
    def get(self):
        """
        Usage
        -----
        Get all tickets based on query and user role.
        Sorting and filtering will be applied as per query.
        Student needs all tickets while searching and needs all their tickets (created and upvoted)
        Support needs pending tickets while resolving and needs all their resolved tickets
        Admin needs resolved tickets while creating FAQ

        Parameters
        ----------
        query

        Returns
        -------
        List of tickets
        """

        # user is student and is searching tickets while creating a new ticket.
        # get query arguments
        try:
            args = request.args.to_dict(flat=True)
            args = ticket_utils.get_args_from_query(args)
        #     user_id = request.headers.get("user_id", "")
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        # user = Authentication.query.filter_by(
        #     user_id=user_id
        # ).first()  # user already exists as user_required verified it

        # # verify is user is student
        # if user.role != "student":
        #     raise PermissionDenied(
        #         status_msg="Only student can search all tickets using query."
        #     )

        all_tickets = []

        # get all tickets
        tickets = Ticket.query.all()
        for ticket in tickets:
            tick = ticket_utils.convert_ticket_to_dict(ticket)
            all_tickets.append(tick)

        all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)

        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)

#start working from here 
# Also had other APIs
class AllTicketsUserAPI(Resource):
    @token_required
    @users_required(users=["Student", "Staff", "Admin"])
    def get(self, user_id=""):
        # tickets retrieved based on user role.

        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # get query arguments
        try:
            args = request.args.to_dict(flat=True)

            args = ticket_utils.get_args_from_query(args)
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        user = User.query.filter_by(id=user_id
        ).first()  # user already exists as user_required verified it

        all_tickets = []

        # verify user role
        role = user.role.name

        if role == "Student":
            # student : all tickets created or upvoted by him/her
            # status, priority, sort, filter will be as per filter options received
            # upvoted ticket can be checked by comparing created_by with user_id
            upvoted_ticket_ids = VoteTable.query.filter_by(voter_id=user.id).all()
            upvoted_ticket_ids = [elem.ticket_id for elem in upvoted_ticket_ids]
            user_tickets = Ticket.query.filter_by(user_id=user.id).all()
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)
            for ticket_id in upvoted_ticket_ids:
                ticket = Ticket.query.filter_by(id=ticket_id).first()
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        if role == "Staff":
            # support : all tickets resolvedby him/her
            # get all pending tickets
            # status, priority, sort, filter will be as per filter options received

            if "Resolved" in args["status"]:
                # get all tickets resolved by the support staff
                user_tickets = Ticket.query.filter_by(resolved_by=user.id).all()
            elif "Open" in args["status"]:
                # get all pending tickets
                user_tickets = Ticket.query.filter_by(ticket_status="Open").all()
            else:
                user_tickets = []
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        if role == "Admin":
            # admin : get all tickets resolved globally (for creating faq)
            # status, priority, sort, filter will be as per filter options received
            user_tickets = Ticket.query.filter_by(ticket_status="Resolved").all()
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)
        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)


ticket_api.add_resource(
    TicketAPI,
    "/<string:ticket_id>/<string:user_id>",
    "/<string:user_id>",
)  # path is /api/v1/ticket
ticket_api.add_resource(AllTicketsAPI, "/all-tickets")
ticket_api.add_resource(AllTicketsUserAPI, "/all-tickets/<string:user_id>")

# --------------------  --------------------

# - get comments of a ticket %
# - post comment &
# - edit comment &
# - delete comment &


class TicketCommentAPI(Resource):
    def get(self, ticket_id=""):
        if ticket_utils.is_blank(ticket_id) :
            raise BadRequest(status_msg="Ticket id is missing.")

        # check if ticket exists
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketCommentAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                ticket_comments = []
                comments = TicketComments.query.filter_by(ticket_id=ticket.id).all()
                for comment in comments: 
                    c = ticket_utils.get_ticket_comments(comment)
                    #ticket_comments = ticket_utils.get_ticket_comments(comments) #issue stemming from this function
                    ticket_comments.append(c)
                return success_200_custom(data=ticket_comments)
            else:
                raise NotFoundError(status_msg="Ticket does not exists")
        
    def post(self, ticket_id=""):
        
        details = {
            "comment": "",
            "commenter" : "",
            "user_mentions" : [],
            "reactions" : ""
        }
        if ticket_utils.is_blank(ticket_id):
            raise BadRequest(status_msg="Ticket id is missing.")

        # check if ticket exists
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketCommentAPI->post : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket: 
                try:
                    form = request.get_json()
                    for key in details:
                        value = form.get(key, "")
                        details[key] = value
                except Exception as e:
                    logger.error(
                        f"TicketCommentAPI->post : Error occured while getting form data : {e}"
                    )
                    raise InternalServerError
                else:
                    details["added_at"] = time_to_str(datetime.datetime.now())
                    details["ticket_id"] = ticket_id
                    comment = TicketComments(**details)
                    try:
                        db.session.add(comment)
                        db.session.commit()
                    except Exception as e:
                        logger.error(
                            f"TicketCommentAPI->post : Error occured while commenting : {e}"
                        )
                        raise InternalServerError(
                            status_msg="Error occured while commenting"
                        )
                    else:
                        logger.info("Commented successfully.")
                        raise Success_200(status_msg="Ticket comment added successfully.")
            else: 
                raise NotFoundError(status_msg="Ticket does not exists")

#ISSUE - commenter updating to null every time the put method is called
    def put(self, comment_id=-1, ticket_id="", user_id=""):
        details = {
            "comment": "",
            "user_mentions" : [],
            "reactions" : ""
        }
        if ticket_utils.is_blank(ticket_id) or comment_id == -1:
            raise BadRequest(status_msg="Ticket id or comment id is missing.")

        # check if ticket exists
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketCommentAPI->post : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket: 
                try:
                    form = request.get_json()
                    for key in details:
                        value = form.get(key, "")
                        details[key] = value
                except Exception as e:
                    logger.error(
                        f"TicketCommentAPI->put : Error occured while getting form data : {e}"
                    )
                    raise InternalServerError
                else:
                    try:
                        comment = TicketComments.query.filter_by(id=comment_id).first()
                    except Exception as e:
                        logger.error(
                            f"TicketCommentAPI->put : Error occured while fetching the comment : {e}"
                        )
                        raise InternalServerError
                    else: 
                        print(comment.commenter)
                        if comment and comment.commenter == user_id: 
                            comment.comment = details['comment']
                            comment.commenter = user_id
                            comment.user_mentions = details["user_mentions"]
                            comment.reactions = details["reactions"]
                    try:
                        db.session.commit()
                    except Exception as e:
                        logger.error(
                            f"TicketCommentAPI->put : Error occured while updating comment : {e}"
                        )
                        raise InternalServerError(
                            status_msg="Error occured while updating comment"
                        )
                    else:
                        logger.info("Comment updated successfully.")
                        raise Success_200(status_msg="Ticket comment updated successfully.")
            else: 
                raise NotFoundError(status_msg="Ticket does not exists")
        #raise Success_200(status_msg="Ticket Comment updated successfully")


    def delete(self, ticket_id="", comment_id=-1, user_id=""):
        if ticket_utils.is_blank(ticket_id) :
            raise BadRequest(status_msg="Ticket id is missing.")
        
        try: 
            ticket = Ticket.query.filter_by(id=ticket_id).first()
        except: 
            logger.error(f"TicketCommentAPI->get : Error occured while fetching ticket data : {e}")
            raise InternalServerError
        else: 
            if ticket: 

                try:
                    comment = TicketComments.query.filter_by(id=comment_id).first()
                except Exception as e:
                    logger.error(
                        f"TicketCommentAPI->delete : Error occured while fetching the comment : {e}"
                    )
                    raise InternalServerError
                else:
                    if comment and comment.commenter == user_id:
                        db.session.delete(comment)
                        db.session.commit()
                        raise Success_200(status_msg="Comment Deleted")
                    else:
                        raise NotFoundError(status_msg="Comment Does Not Exist")

ticket_api.add_resource(TicketCommentAPI, "/comments/<string:ticket_id>", endpoint="ticket_comment")
ticket_api.add_resource(TicketCommentAPI, "/comments/<string:ticket_id>/<int:comment_id>/<string:user_id>", endpoint="comment_update_delete")
#ticket_api.add_resource(TicketCommentAPI, "/comments/<string:ticket_id>/<int:comment_id>/", endpoint="comment_delete")




