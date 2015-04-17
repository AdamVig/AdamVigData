import datetime

def get_date():
    """Returns today's date in format MM-DD-YY"""
    today = datetime.datetime.today()
    date_format = "%m/%d/%y %I:%M %p"
    return today.strftime(date_format)
