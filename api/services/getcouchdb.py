import couchdb, datetime

def get_couch_db():
    """Get Couch database from server"""

    auth = "arkincesselsesentemblefo:BUeaRWc0yVBD2wMINyKrgNiy@"
    server = couchdb.Server("https://" + auth + "adamvig.cloudant.com/")
    db = server['gocostudent']
    return db

def get_app_info(db=get_couch_db()):
    """Get info doc from database"""

    return db['info']

def get_user(username, db=get_couch_db()):
    """Get user from database"""

    user = db.get(username)
    return user

def save_user(user, db=get_couch_db()):
    """Save user in database or update existing user"""

    user = db.save(user)
    return user

def log_usage(username, data_type):
    """Log usage"""

    db = get_couch_db()
    user = get_user(username, db)

    if 'dataRequests' in user:

        # Increment or create number of requests for data type
        if data_type in user['dataRequests']:
            user['dataRequests'][data_type] += 1
        else:
            user['dataRequests'][data_type] = 1
    else:
        user['dataRequests'] = {
            data_type: 1
        }

    if 'lastLogin' in user:
        today = datetime.datetime.today()
        date_format = "%m/%d/%y %I:%M %p"
        user['lastLogin'] = today.strftime(date_format)

    if 'totalLogins' in user:
        user['totalLogins'] += 1

    save_user(user, db)
