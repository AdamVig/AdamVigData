"""Get Gordon Athletics schedule."""
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import arrow
import config
from api.services import db

URL = "http://athletics.gordon.edu/calendar.ashx/calendar.rss"
CACHE_KEY = "athleticsSchedule"

# Create fake header to circumvent user agent filtering
HEADERS = {'User-Agent': UserAgent().chrome}


def get_athletics_schedule(username, password):
    """Get Gordon Athletics schedule."""
    time_now = arrow.now(config.TIMEZONE)
    athletics_schedule = get_cached_athletics_schedule()

    # Get expiration time from cached data
    try:
        time_expiration = arrow.get(
            athletics_schedule['expiration'],
            config.DATETIME_FORMAT)
    except arrow.parser.ParserError:
        time_expiration = None

    # If data is expired, get fresh data from website
    if time_now > time_expiration:
        try:
            response = requests.get(URL, headers=HEADERS)
            response.raise_for_status()
        except Exception as err:
            raise ValueError("Could not retrieve athletics calendar: " + err)
        else:
            athletics_schedule['schedule'] = parse_athletics_rss(response.text)
            db.cache_app_data(CACHE_KEY,
                              athletics_schedule,
                              config.UPDATE_INTERVAL['ATHLETICS_SCHEDULE'])
    return {
        'data': athletics_schedule['schedule']
    }


def parse_athletics_rss(feed):
    """Parse athletics RSS feed into a list.

    The feed follows the RSS spec, with <rss> containing a <channel> tag
    containing a list of <item> tags.
    """
    rss_data = BeautifulSoup(feed)
    athletics_schedule = []

    for item in rss_data.find_all('item'):
        event = parse_athletics_event(item)
        if event is not None:
            athletics_schedule.append(event)

    return athletics_schedule


def parse_athletics_event(item):
    """Parse athletics event into a dict with only the desired data.

    Each <item> tag represents an athletic event and contains the following:
    title, description, link, ev:gameid, ev:location, ev:startdate, ev:enddate,
    s:localstartdate, s:localenddate, s:teamlogo, s:opponentlogo

    Title is prefixed by the date in M/D format.
    Description is suffixed by a newline and a permalink.
    Dates are in either YYYY-MM-DD or Unix timestamp format.
    """
    title = get_tag_string(item, 'description')
    title = title.split('\\n')[0].strip()  # Only get first line of description

    url = get_tag_string(item, 'guid')
    location = get_tag_string(item, 'ev:location')
    opponent_logo_url = get_tag_string(item, 's:opponentlogo')

    local_start_date = get_tag_string(item, 's:localstartdate')
    datetime = arrow.get(local_start_date)
    datetime_string = datetime.format(config.DATETIME_FORMAT)
    datetime_relative = date.make_relative_date(datetime)

    event = {
        'title': title,
        'url': url,
        'location': location,
        'opponentLogoURL': opponent_logo_url,
        'datetime': datetime_string,
    }

    # Replace empty string values with explanatory string
    string_keys = ['title', 'location', 'time']
    error_explanation = "Unknown"
    for key, value in event.iteritems():
        if key in string_keys and value is None:
            event[key] = error_explanation

    # Only return event if it has not happened yet
    if datetime > arrow.now():
        return event


def get_tag_string(item, tag_name):
    """Get tag string from a given BeautifulSoup item."""
    tag = item.find(tag_name)

    if tag is None:
        raise ValueError("Could not find " + tag_name + " in given item.")

    return tag.string


def get_cached_athletics_schedule():
    """Get cached athletics schedule from database."""
    try:
        return db.get_doc('cache')[CACHE_KEY]
    except KeyError:
        print "Could not find cached athletics schedule."
        raise
