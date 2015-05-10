from config import *
import couchdb, getdate, httplib

def get_db():
    """Get Couch database from server"""

    auth = COUCH_USER + ":" + COUCH_PASS + "@"
    server = couchdb.Server("https://" + auth + COUCH_SERVER)
    db = server[COUCH_DB_NAME]
    return db

def get_app_info(db=get_db()):
    """Get info doc from database"""

    return db['info']

def get_user(username, db=get_db()):
    """Get user from database"""

    user = db.get(username)
    if user is not None:
        return user
    else:
        raise ValueError("User does not exist.", httplib.NOT_FOUND)

def save_user(user, db=get_db()):
    """Save user in database or update existing user"""
    try:
        updated_user = db.save(user)
    except couchdb.ResourceConflict as err:
        raise couchdb.ResourceConflict("Document updated conflict on " + \
            user.get('_id'))
    else:
        return updated_user

def log_usage(username, data_type, app_version, data):
    """Log usage and cache data"""

    db = get_db()

    try:
        user = get_user(username, db)
    # User does not exist
    except ValueError as err:
        create_user(username, app_version)
    # User exists
    else:
        # Increment or create number of requests for data type
        if 'dataRequests' in user:
            if data_type in user['dataRequests']:
                user['dataRequests'][data_type] += 1
            else:
                user['dataRequests'][data_type] = 1
        else:
            user['dataRequests'] = {}
            user['dataRequests'][data_type] = 1

        # Set last login time to now
        user['lastLogin'] = getdate.get_date()

        # Set app version
        user['appVersion'] = app_version

        # Increment total logins
        if 'totalLogins' in user:
            user['totalLogins'] += 1
        else:
            user['totalLogins'] = 1

        # Cache data
        if 'dataCache' in user:
            user['dataCache'][data_type] = data['data'];
        else:
            user['dataCache'] = {}
            user['dataCache'][data_type] = data['data'];

        try:
            save_user(user, db)
        except couchdb.ResourceConflict as err:
            print "Could not log usage due to document update conflict on " + \
                user.get('_id')


def create_user(username, app_version):
    """Create new user in database"""

    db = get_db()

    try:
        get_user(username, db)
    # User does not exist
    except ValueError as err:
        user = {
            '_id': username,
            'firstLogin': getdate.get_date(),
            'lastLogin': getdate.get_date(),
            'appVersion': app_version,
            'totalLogins': 0,
            'dataRequests': {}
        }
        save_user(user, db)
        return {
            'data': user
        }
    # User already exists
    else:
        raise ValueError("User already exists.", httplib.CONFLICT)
