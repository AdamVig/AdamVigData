"""Mark all users inactive in the database."""
from api.services import *
from config import *
import sys

reserved_ids = ['cache', 'info', 'message']
database = db.get_db()
active_users = 0
inactive_users = 0
total_users = 0

print 'Working...',
for doc_id in database:
    print '.',
    if doc_id not in reserved_ids:
        doc = db.get_doc(doc_id, database)

        # Count number of users
        total_users += 1
        if 'active' in doc:
            if doc['active'] is True:
                active_users += 1
            elif doc['active'] is False:
                inactive_users += 1

            if 'totalLogins' in doc:
                if doc['totalLogins'] == 0:
                    doc['active'] = False
                    database.save(doc)
                    print
                    print "Marked", doc_id, "as inactive."
        else:
            print
            print "Doc with id", doc_id, "is missing 'active' field."
    sys.stdout.flush()

print "Total Users:", total_users
print "Inactive Users:", inactive_users
print "Active Users:", active_users
