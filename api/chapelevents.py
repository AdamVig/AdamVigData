"""Get chapel events from Go Gordon."""
import mechanize
import httplib
import urllib2
import arrow
from bs4 import BeautifulSoup
from services import db
from config import *


def get_next_chapel_event(username, password):
    """Get next chapel event."""
    next_chapel_event = None
    next_chapel_event_time = None
    all_chapel_events = get_chapel_events(username, password)['data']
    time_now = arrow.now(TIMEZONE)

    for event in all_chapel_events:
        event_date = event['date'] + ' ' + event['time']
        try:
            event_datetime = arrow.get(event_date, chapel_date_format)
        except arrow.parser.ParserError:
            event_datetime = None

        if event_datetime is not None:

            # Set next event time to arbitrary datetime
            if not next_chapel_event_time:
                next_chapel_event_time = event_datetime

            # If event has not already happened and is before next_chapel_event
            if (event_datetime > time_now and
                    event_datetime < next_chapel_event_time):
                next_chapel_event = event['title']
                next_chapel_event_time = event_datetime

    return {
        'data': next_chapel_event,
        'eventTime': next_chapel_event_time.format(date_format)
    }


def get_chapel_events(username, password):
    """Get list of all chapel events from Go Gordon."""
    chapel_events = get_cached_chapel_events()

    try:
        time_expiration = arrow.get(
            chapel_events['expiration'],
            DATETIME_FORMAT)
    except arrow.parser.ParserError:
        time_expiration = None
    time_now = arrow.now(TIMEZONE)

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
            all_chapel_events = []

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
                event_title = smart_truncate(event_title, 30)

                chapel_time_format = 'mm:hh A'
                event_time = chapel_event.find_all('td')[3].text.strip()
                event_time = arrow.get(event_time, chapel_time_format)

                chapel_date_format = 'MM/DD/YYYY'
                event_date = chapel_event.find_all('td')[2].text.strip()
                event_date = arrow.get(event_date, chapel_date_format)

                event_data = {
                    'title': event_title,
                    'date': event_date.format(DATE_FORMAT),
                    'time': event_time.format(TIME_FORMAT),
                }

                all_chapel_events.append(event_data)

            chapel_events = {'events': all_chapel_events}

            db.cache_app_data('chapelEvents',
                              chapel_events,
                              CHAPEL_EVENTS_UPDATE_INTERVAL_MINUTES)

    return {
        'data': chapel_events['events']
    }


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
