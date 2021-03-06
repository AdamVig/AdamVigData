"""Get chapel events from Go Gordon."""
import mechanize
import httplib
import urllib2
import arrow
from bs4 import BeautifulSoup
from api.services import db
from api.services import date
import config

CHAPEL_DATE_FORMAT = 'MM/DD/YYYY'
CHAPEL_TIME_FORMAT = 'hh:mm A'
CHAPEL_DATETIME_FORMAT = CHAPEL_DATE_FORMAT + \
    ' ' + CHAPEL_TIME_FORMAT


def get_chapel_events(username, password):
    """Get list of all chapel events from Go Gordon."""
    chapel_events = get_cached_chapel_events()

    try:
        time_expiration = arrow.get(
            chapel_events['expiration'],
            config.DATETIME_FORMAT)
    except arrow.parser.ParserError:
        time_expiration = None
    time_now = arrow.now(config.TIMEZONE)

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
                raise ValueError(config.ERROR_INFO['UNAUTHORIZED'])
            else:
                raise ValueError(config.ERROR_INFO['INTERNAL_SERVER_ERROR'])

        except Exception:
            raise ValueError(config.ERROR_INFO['INTERNAL_SERVER_ERROR'])
        else:
            chapel_events = parse_chapel_events(browser)

            db.cache_app_data('chapelEvents',
                              chapel_events,
                              config.UPDATE_INTERVAL['CHAPEL_EVENTS'])

    return {
        'data': chapel_events['events']
    }


def get_cached_chapel_events():
    """Get cached chapel events from database."""
    return db.get_doc('cache')['chapelEvents']


def parse_chapel_events(browser):
    """Parse chapel events from retrieved page."""
    page = BeautifulSoup(browser.response().read())
    all_chapel_events = []

    # Get list of all chapel events
    chapel_events_table = page \
        .find_all('table')[-1] \
        .find_all('tr')

    del chapel_events_table[0]  # Remove header row

    # Convert table into readable data format
    for chapel_event in chapel_events_table:
        event_title = chapel_event     \
                    .find_all('td')[1] \
                    .find_all('a')[0]  \
                    .text              \
                    .strip()

        # Get event date
        event_date = chapel_event.find_all('td')[2].text.strip()
        event_datetime = event_date
        event_date = arrow.get(event_date, CHAPEL_DATE_FORMAT)

        # Get event time
        event_time = chapel_event.find_all('td')[3].text.strip()
        event_datetime += ' ' + event_time
        event_time = arrow.get(event_time, CHAPEL_TIME_FORMAT)

        # Create datetime
        event_datetime = arrow.get(event_datetime,
                                   CHAPEL_DATETIME_FORMAT)

        # Create description of how long until event
        event_relative = date.make_relative_date(event_datetime)

        event_data = {
            'title': event_title,
            'date': event_date.format(config.DISPLAY_DATE_FORMAT),
            'time': event_time.format(config.DISPLAY_TIME_FORMAT),
            'datetime': event_datetime.format(
                config.DISPLAY_DATETIME_FORMAT),
            'relative': event_relative
        }

        all_chapel_events.append(event_data)

    return {'events': all_chapel_events}
