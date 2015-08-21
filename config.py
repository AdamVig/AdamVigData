"""Configuration parameters for the app."""
DEBUG = False
TESTING = False

WENHAM_LATITUDE = 42.587576
WENHAM_LONGITUDE = -70.824631
WEATHER_UPDATE_INTERVAL_MINUTES = 15

PAPERTRAIL_URL = 'logs2.papertrailapp.com'
PAPERTRAIL_PORT = 26735

DATE_FORMAT = '%m/%d/%y %I:%M %p'
LOG_FORMAT = '[%(levelname)s] %(message)s'

END_POINT_PREFIX = '/gocostudent/<version>/'

# Emoji
emoji = {
    "SAD_FACE": u'\U0001F62D',
    "SOS": u'\U0001F198',
    "CLAPPING": u'\U0001F44F',
    "SHRUG": u'\U0001F481'
}

# Error messages should be 22 characters max
error_message = {
    "INTERNAL_SERVER_ERROR": "Something went wrong! " + emoji['SOS'],
    "NOT_FOUND":             "Couldn't find data. " + emoji['SAD_FACE'],
    "UNAUTHORIZED":          "Your login is wrong. " + emoji['SHRUG']
}

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
