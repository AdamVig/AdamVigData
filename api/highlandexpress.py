"""Get Highland Express data."""
from config import ERROR_INFO, TIMEZONE
from api.services import db
import arrow
import couchdb
import requests

URL = "https://gocostudent.adamvig.com/api/highlandexpress"

def get_highland_express(username, password):
    """Get Highland Express data."""
    try:
        r = requests.get(URL)
        highland_data = r.json()['data']
        print highland_data
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
    print "This API is deprecated! Use new Highland Express API instead.:", err
    raise ValueError(ERROR_INFO['INTERNAL_SERVER_ERROR'])


def decide_schedule_day():
    """Decide which schedule to use for today."""
    day_of_week = arrow.now(TIMEZONE).format('dddd').lower()
    if day_of_week in "mondaytuesdaywednesdaythursday":
        return "weekday"
    else:
        return day_of_week
