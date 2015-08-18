"""Get today's date."""
from config import *
from datetime import datetime
from pytz import timezone


def get_date():
    """Get today's date in format MM-DD-YY."""
    # Format for date output

    # Datetime in Eastern timezone
    eastern = timezone('US/Eastern')
    eastern_today = datetime.now(eastern)

    return eastern_today.strftime(DATE_FORMAT)


def get_date_time_object():
    """Get current date and time as a date time object."""
    eastern = timezone('US/Eastern')
    return datetime.now(eastern)


def parse_date_time(date_time):
    """Parse a date time string into a date time object."""
    eastern = timezone('US/Eastern')
    parsed = datetime.strptime(date_time, DATE_FORMAT)
    return eastern.localize(parsed)
