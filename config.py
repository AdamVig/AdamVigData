"""Configuration parameters for the app."""
import httplib

DEBUG = False
TESTING = False

WENHAM_LATITUDE = 42.587576
WENHAM_LONGITUDE = -70.824631

# Time to wait between cache updates, in minutes
UPDATE_INTERVAL = {
    "WEATHER": 15,
    "CHAPEL_EVENTS": 60,
    "ATHLETICS_SCHEDULE": 60
}

PAPERTRAIL_URL = 'logs2.papertrailapp.com'
PAPERTRAIL_PORT = 26735

DATE_FORMAT = 'MM/DD/YY'
TIME_FORMAT = 'hh:mm A'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT
DISPLAY_DATE_FORMAT = 'MMM D'
DISPLAY_TIME_FORMAT = 'h:mm A'
DISPLAY_DATETIME_FORMAT = DISPLAY_DATE_FORMAT + ' ' + DISPLAY_TIME_FORMAT

TIMEZONE = 'US/Eastern'
LOG_FORMAT = '[%(levelname)s] %(message)s'

END_POINT_PREFIX = '/gocostudent/<version>/'

# EMOJI
EMOJI = {
    "SAD_FACE": u'\U0001F62D',
    "SOS": u'\U0001F198',
    "CLAPPING": u'\U0001F44F',
    "SHRUG": u'\U0001F481',
    "CROSSED_SWORDS": u'\U00002694'
}

# Key must be name of HTTP status code from httplib,
#   see complete list here: https://docs.python.org/2/library/httplib.html
# Value must be 22 characters or fewer
ERROR_MESSAGE = {
    # Character measurement: 0_____________________23
    "INTERNAL_SERVER_ERROR": "Something went wrong! " + EMOJI['SOS'],
    "NOT_FOUND":             "Couldn't find data. " + EMOJI['SAD_FACE'],
    "UNAUTHORIZED":          "Your login is wrong. " + EMOJI['SHRUG'],
    "CONFLICT":              "Could not save data. " + EMOJI['CROSSED_SWORDS']
}

# Construct dictionary of tuples of error messages and codes
ERROR_INFO = {}
for error_name, error_message in ERROR_MESSAGE.iteritems():
    error_code = getattr(httplib, error_name)
    ERROR_INFO[error_name] = (error_message, error_code)

# Get API keys and server info either from local file or environment variables
try:
    import keys
except ImportError as err:
    import os
    COUCH_SERVER = os.environ.get('COUCH_SERVER')
    COUCH_DB_NAME = os.environ.get('COUCH_DB_NAME')
    COUCH_USER = os.environ.get('COUCH_USER')
    COUCH_PASS = os.environ.get('COUCH_PASS')
    FORECASTIO_API_KEY = os.environ.get('FORECASTIO_API_KEY')
else:
    COUCH_SERVER = keys.COUCH_SERVER
    COUCH_DB_NAME = keys.COUCH_DB_NAME
    COUCH_USER = keys.COUCH_USER
    COUCH_PASS = keys.COUCH_PASS
    FORECASTIO_API_KEY = keys.FORECASTIO_API_KEY
