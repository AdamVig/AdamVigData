"""Mark all users inactive in the database."""
from api.services import *

reserved_ids = ['cache', 'info', 'message']
database = db.get_db()

for doc_id in database:
    if doc_id not in reserved_ids:
        doc = db.get_doc(doc_id, database)
        if 'totalLogins' in doc:
            if doc['totalLogins'] == 0:
                doc['active'] = False
                database.save(doc)
                print "Marked " + doc_id + " as inactive."
        else:
            print "User " + doc_id + " does not have a totalLogins field."
