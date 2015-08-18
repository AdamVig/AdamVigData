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
