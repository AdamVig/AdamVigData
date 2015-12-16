"""Handle operations on datetime objects."""
from datetime import datetime


def make_relative_date(date_time):
    """Make a relative date string from a datetime."""
    current_date_time = datetime.now()
    time_until = date_time.naive - current_date_time
    hours_until = time_until.days * 24 + time_until.seconds // 3600

    # If any time next week, get weekday names
    if time_until.days > 1 and time_until.days < 7:
        relative_date = date_time.format('dddd')

        # Prepend 'next' to weekday name if next week
        current_week_number = current_date_time.isocalendar()[1]
        week_number = date_time.isocalendar()[1]
        if week_number > current_week_number:
            relative_date = "next " + relative_date

    # If under 24 hours until and not current day, return "tomorrow"
    elif (hours_until < 24 and
          date_time.datetime.day != current_date_time.day):
        relative_date = "tomorrow"

    # Otherwise use default humanize output
    else:
        # Explicit use of current time to prevent timezone errors
        relative_date = date_time.humanize(current_date_time)

        if relative_date == "in a day":
            relative_date = "tomorrow"

    return relative_date
