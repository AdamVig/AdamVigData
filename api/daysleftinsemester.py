from datetime import datetime
from services import db

def get_days_left_in_semester(username, password):
    """Get number of days left in semester"""

    date_format = "%m/%d/%Y"
    app_info = db.get_app_info()
    last_date = datetime.strptime(app_info['lastDayOfSemester'], date_format)

    delta = last_date - datetime.today()
    num_days = delta.days - 1

    if num_days < 0:
        num_days = 0;

    return { 'data': num_days }
