"""Get today's date."""
from datetime import datetime
from pytz import timezone


def get_date():
    """Get today's date in format MM-DD-YY."""
    # Format for date output
    date_format = "%m/%d/%y %I:%M %p"

    # Datetime in Eastern timezone
    eastern = timezone('US/Eastern')
    eastern_today = datetime.now(eastern)

    return eastern_today.strftime(date_format)
