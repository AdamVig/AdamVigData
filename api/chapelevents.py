"""Get chapel events from Go Gordon."""
import mechanize
import httplib
import urllib2
import arrow
from datetime import datetime
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
                chapel_date_format = 'MM/DD/YYYY'
                event_date = chapel_event.find_all('td')[2].text.strip()
                event_datetime = event_date
                event_date = arrow.get(event_date, chapel_date_format)

                # Get event time
                chapel_time_format = 'hh:mm A'
                event_time = chapel_event.find_all('td')[3].text.strip()
                event_datetime += ' ' + event_time
                event_time = arrow.get(event_time, chapel_time_format)

                # Create datetime
                chapel_datetime_format = chapel_date_format + \
                    ' ' + chapel_time_format
                event_datetime = arrow.get(event_datetime,
                                           chapel_datetime_format)

                # Create description of how long until event
                # Add five hours to event_datetime to fix timezone problem
                event_relative = make_relative_date(event_datetime
                                                    .replace(hours=+5))

                event_data = {
                    'title': event_title,
                    'date': event_date.format(DISPLAY_DATE_FORMAT),
                    'time': event_time.format(DISPLAY_TIME_FORMAT),
                    'datetime': event_datetime.format(DISPLAY_DATETIME_FORMAT),
                    'relative': event_relative
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


def make_relative_date(date_time):
    """Make a relative date string from a datetime."""
    current_date_time = datetime.now()
    time_until = date_time.naive - current_date_time
    hours_until = time_until.days * 24 + time_until.seconds // 3600

    # If any time next week, get weekday names
    if time_until.days > 1 and time_until.days < 7:
        relative_date = date_time.format('dddd')

        # Prepend 'next' to weekday name if next week
        current_week_number = current_date_time.isocalendar()[1]
        week_number = date_time.isocalendar()[1]
        if week_number > current_week_number:
            relative_date = "next " + relative_date

    # If under 24 hours until and not current day, return "tomorrow"
    elif (hours_until < 24 and
          date_time.datetime.day != current_date_time.day):
        relative_date = "tomorrow"

    # Otherwise use default humanize output
    else:
        relative_date = date_time.humanize()

        if relative_date == "in a day":
            relative_date = "tomorrow"

    return relative_date
