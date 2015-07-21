"""Configuration parameters for the app."""
DEBUG = False
TESTING = False

COUCH_SERVER = 'adamvig.cloudant.com'
COUCH_DB_NAME = 'gocostudent'

WENHAM_LATITUDE = 42.587576
WENHAM_LONGITUDE = -70.824631

PAPERTRAIL_URL = 'logs2.papertrailapp.com'
PAPERTRAIL_PORT = 26735

LOG_FORMAT = '[%(levelname)s] %(message)s'

END_POINT_PREFIX = '/gocostudent/<version>/'

# Get API keys either from local file or environment variables
try:
    import keys
except ImportError as err:
    import os
    COUCH_USER = os.environ.get('COUCH_USER')
    COUCH_PASS = os.environ.get('COUCH_PASS')
    FORECASTIO_API_KEY = os.environ.get('FORECASTIO_API_KEY')
else:
    COUCH_USER = keys.COUCH_USER
    COUCH_PASS = keys.COUCH_PASS
    FORECASTIO_API_KEY = keys.FORECASTIO_API_KEY
