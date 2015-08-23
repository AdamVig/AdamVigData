"""Interface with database."""
from config import *
import couchdb
import getdate
import httplib
from datetime import timedelta


def get_db():
    """Get Couch database from server."""
    auth = COUCH_USER + ":" + COUCH_PASS + "@"
    server = couchdb.Server("https://" + auth + COUCH_SERVER)
    db = server[COUCH_DB_NAME]
    return db


def get_doc(doc_id, db=get_db()):
    """Get doc from database by id."""
    doc = db[doc_id]
    if doc is not None:
        return doc
    else:
        raise ValueError("Doc does not exist.", httplib.NOT_FOUND)


def save_user(user, db=get_db()):
    """Save user in database or update existing user."""
    try:
        updated_user = db.save(user)
    except couchdb.ResourceConflict:
        raise couchdb.ResourceConflict("Document updated conflict on " +
                                       user.get('_id'))
    else:
        return updated_user


def save_app_info(key, data, db=get_db()):
    """Save app info in the info doc."""
    app_info = get_doc('info', db)
    app_info[key] = data
    db.save(app_info)


def cache_app_data(data_type, data, update_interval_minutes, db=get_db()):
    """Cache app data in the cache doc with expiration date."""
    app_cache = get_doc('cache', db)
    now = getdate.get_date_time_object()
    expiration_time = now + timedelta(minutes=update_interval_minutes)

    data['expiration'] = getdate.make_datetime_string(expiration_time)

    app_cache[data_type] = data
    db.save(app_cache)


def log_usage(username, data_type, app_version, data, should_cache=True):
    """Log usage and cache data."""
    db = get_db()

    try:
        user = get_doc(username, db)
    # User does not exist
    except ValueError:
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

        # Set last login time to now and mark as active
        user['lastLogin'] = getdate.get_date()
        user['active'] = True

        # Set app version
        user['appVersion'] = app_version

        # Increment total logins
        if 'totalLogins' in user:
            user['totalLogins'] += 1
        else:
            user['totalLogins'] = 1

        # Cache data if caching is enabled for this data type
        if should_cache is True:
            user = cache_data(user, data_type, data)

        try:
            save_user(user, db)
        except couchdb.ResourceConflict:
            print "Could not log usage due to document update conflict on " + \
                user.get('_id')


def cache_data(user, data_type, data):
    """Cache requested data in user data."""
    # If user has accepted/denied privacy policy
    if 'privacyPolicy' in user:
        if user['privacyPolicy'] == 'accepted':

            # Cache data in existing data cache field
            if 'dataCache' in user:
                user['dataCache'][data_type] = data['data']

            # Create data cache field
            else:
                user['dataCache'] = {}
                user['dataCache'][data_type] = data['data']

        elif user['privacyPolicy'] == 'denied':
            user = remove_data_cache(user)

    # If user has not seen privacy policy
    else:
        user = remove_data_cache(user)

    return user


def remove_data_cache(user):
    """Remove data cache field from user."""
    user.pop('dataCache', None)
    return user


def set_property(username, property_name, value):
    """Set property in user data."""
    try:
        user = get_doc(username)
    except ValueError:
        raise ValueError("Could not disable caching; user does not exist.",
                         httplib.NOT_FOUND)
    else:
        user[property_name] = value
        try:
            save_user(user)
        except couchdb.ResourceConflict:
            print "Couldn't disable caching due to doc update conflict on " + \
                user.get('_id')
        else:
            return user


def create_user(username, app_version):
    """Create new user in database."""
    db = get_db()

    try:
        user = get_doc(username, db)
    # User does not exist
    except ValueError:
        user = {
            '_id': username,
            'firstLogin': getdate.get_date(),
            'lastLogin': getdate.get_date(),
            'appVersion': app_version,
            'totalLogins': 0,
            'dataRequests': {}
        }
        save_user(user, db)

    return {'data': user}
