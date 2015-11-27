"""Get Highland Express data."""
from config import ERROR_MESSAGE
from api.services import db
import httplib


def get_highland_express(username, password):
    """Get Highland Express data."""
    try:
        highland_data = db.get_doc('highlandexpress')
    except ValueError:
        print "Highland Express doc is missing!"
        raise ValueError(ERROR_MESSAGE['NOT_FOUND'], httplib.NOT_FOUND)

    return {
        'data': highland_data
    }
