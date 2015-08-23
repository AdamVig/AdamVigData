"""Get description of next chapel event from Go Gordon."""
import mechanize
import httplib
import urllib2
from bs4 import BeautifulSoup
from services import db
from services import getdate
from config import *

chapel_date_format = '%m/%d/%Y %I:%M %p'


def get_next_chapel_event(username, password):
    """Get description of next chapel event."""
    next_chapel_event = None
    next_chapel_event_time = None
    all_chapel_events = get_all_chapel_events(username, password)
    time_now = getdate.get_date_time_object()

    for event_date, event_description in all_chapel_events.iteritems():
        event_datetime = getdate.parse_date_time(event_date,
                                                 chapel_date_format)

        if event_datetime is not None:

            # Set next event time to arbitrary datetime
            if not next_chapel_event_time:
                next_chapel_event_time = event_datetime

            # If event has not already happened and is before next_chapel_event
            if (event_datetime > time_now and
                    event_datetime < next_chapel_event_time):
                next_chapel_event = event_description
                next_chapel_event_time = event_datetime

    return {
        'data': next_chapel_event,
        'eventTime': getdate.make_datetime_string(next_chapel_event_time)
    }


def get_all_chapel_events(username, password):
    """Get list of all chapel events from Go Gordon."""
    all_chapel_events = get_cached_chapel_events()

    time_expiration = getdate.parse_date_time(all_chapel_events['expiration'])
    time_now = getdate.get_date_time_object()

    if time_now > time_expiration:
        url = 'https://go.gordon.edu/student/chapelcredits/viewupcoming.cfm'

        # Initialize browser
        browser = mechanize.Browser()
        browser.set_handle_robots(False)

        # Add page authentication
        browser.add_password(url, username, password)

        # Get page
        try:
            browser.open(url)
        except urllib2.HTTPError as err:
            if err.code == httplib.UNAUTHORIZED:
                raise ValueError(error_message['UNAUTHORIZED'],
                                 httplib.UNAUTHORIZED)
            else:
                raise ValueError(error_message['INTERNAL_SERVER_ERROR'],
                                 httplib.INTERNAL_SERVER_ERROR)

        except Exception:
            raise ValueError(error_message['INTERNAL_SERVER_ERROR'],
                             httplib.INTERNAL_SERVER_ERROR)
        else:
            page = BeautifulSoup(browser.response().read())
            all_chapel_events = {}

            chapel_events_table = page \
                .find_all('table')[-1] \
                .find_all('tr')

            del chapel_events_table[0]  # Remove header row

            # Normalize data
            for chapel_event in chapel_events_table:
                event_title = chapel_event     \
                            .find_all('td')[1] \
                            .find_all('a')[0]  \
                            .text              \
                            .strip()

                event_title = smart_truncate(event_title, 50)

                event_date = chapel_event.find_all('td')[2].text.strip()
                event_time = chapel_event.find_all('td')[3].text.strip()

                event_key = event_date + ' ' + event_time

                all_chapel_events[event_key] = event_title

            db.cache_app_data('chapelEvents',
                              all_chapel_events,
                              CHAPEL_EVENTS_UPDATE_INTERVAL_MINUTES)

    return all_chapel_events


def get_cached_chapel_events():
    """Get cached chapel events from database."""
    return db.get_doc('cache')['chapelEvents']


def smart_truncate(content, length=100, suffix='...'):
    """Truncate a string without cutting off in the middle of a word.

    From http://stackoverflow.com/a/250373/1850656
    """
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
