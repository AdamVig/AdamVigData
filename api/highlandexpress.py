"""Get Highland Express data."""
from config import ERROR_INFO, TIMEZONE
from api.services import db
import arrow
import couchdb


def get_highland_express(username, password):
    """Get Highland Express data."""
    try:
        highland_data = db.get_doc('highlandexpress')
    except ValueError:
        print "Highland Express doc is missing!"
        raise ValueError(ERROR_INFO['NOT_FOUND'])
    else:
        highland_data['day'] = decide_schedule_day()
        highland_data['days'] = highland_data['schedule'].keys()
        return {
            'data': highland_data
        }


def update_highland_express(doc):
    """Update Highland Express data in database."""
    try:
        updated_doc = db.update_doc(doc)
    except couchdb.ResourceConflict:
        raise ValueError(ERROR_INFO['CONFLICT'])
    except Exception as err:
        print "Error updating Highland Express doc:", err
        raise ValueError(ERROR_INFO['INTERNAL_SERVER_ERROR'])
    else:
        return {
            "data": updated_doc
        }


def decide_schedule_day():
    """Decide which schedule to use for today."""
    day_of_week = arrow.now(TIMEZONE).format('dddd').lower()
    if day_of_week in "mondaytuesdaywednesdaythursday":
        return "weekday"
    else:
        return day_of_week
