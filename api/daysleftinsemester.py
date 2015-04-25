from datetime import datetime
from services import getcouchdb

def get_days_left_in_semester(username, password):
    """Get number of days left in semester"""

    date_format = "%m/%d/%Y"
    last_date = datetime.strptime(
        getcouchdb.get_app_info()['lastDayOfSemester'],
        date_format)

    delta = last_date - datetime.today()
    num_days = delta.days - 1

    return { 'data': num_days }
