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
from application.common_utils import (
    token_required,
    users_required,
)
from application.views.user_utils import UserUtils
from application.responses import *
from application.models import User, Ticket,VoteTable
from application.globals import *

# --------------------  Code  --------------------

#Sahithi 


#Akriti 


# Muskan 








