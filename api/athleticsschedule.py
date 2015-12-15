"""Get Gordon Athletics schedule."""
from fake_useragent import UserAgent
import requests
import arrow
import config
from api.services import db

URL = "http://athletics.gordon.edu/calendar.ashx/calendar.rss?sport_id=&han="
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
            feed = requests.get(URL)
            athletics_schedule = parse_athletics_rss(feed)
            response = requests.get(URL, headers=HEADERS)
        except Exception as err:
            print "Error getting athletics schedule!"
        else:
            db.cache_app_data(CACHE_KEY,
                              athletics_schedule,
                              config.UPDATE_INTERVAL['ATHLETICS_SCHEDULE'])
    return {
        'data': athletics_schedule
    }


def parse_athletics_rss(feed):
    """Parse athletics RSS feed into a dict."""


def get_cached_athletics_schedule():
    """Get cached athletics schedule from database."""
    return db.get_doc('cache')[CACHE_KEY]
