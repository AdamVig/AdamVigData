"""Mark all users inactive in the database."""
from api.services import *

database = db.get_db()

for doc_id in database:
    if doc_id != 'info':
        doc = db.get_user(doc_id, database)
        doc['active'] = False
        database.save(doc)
        print "Marked " + doc_id + " as inactive."
