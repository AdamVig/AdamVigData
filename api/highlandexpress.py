"""Get Highland Express data."""
from config import error_message
from api.services import db
import httplib


def get_highland_express():
    """Get Highland Express data."""
    try:
        highland_data = db.get_doc('highland-express')
    except ValueError:
        print "Highland Express doc is missing!"
        raise ValueError(error_message['NOT_FOUND'], httplib.NOT_FOUND)

    return {
        'data': highland_data
    }
