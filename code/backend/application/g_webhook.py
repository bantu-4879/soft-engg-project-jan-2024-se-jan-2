from json import dumps
from httplib2 import Http


def gchat_webhook(type, ticket_id):
    """
    Usage
    -----
    1. Sends a message in GChat when a ticket is escalated
    2. Sends a message in GChat when a ticket is marked high priority

    Parameters
    ----------
    type: [escalation, high_priority] (w/ a priority level of 0.7 or higher)
    ticket_id: ticket_id for easy identification

    Returns
    -------

    """

    url = "https://chat.googleapis.com/v1/spaces/AAAAsTbnkos/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=2ZVePrYB_1cEwSrlkdUstzpUGCFBW9a6_RtzylmGdQE"
    if type == "escalation":
        app_message = {"text": "Ticket Escalated! \nID: *" + ticket_id + "*"}
    elif type == "high_priority":
        app_message = {
            "text": "High-Priority Ticket Detected! \nID: *" + ticket_id + "*"
        }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)
