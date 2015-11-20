"""Calculate number of mealpoints per day."""
from mealpoints import get_meal_points
from config import ERROR_MESSAGE
from daysleftinsemester import get_days_left_in_semester
import httplib


def get_meal_points_per_day(username, password):
    """Calculate number of mealpoints per day."""
    meal_points = get_meal_points(username, password).get('data')
    days = get_days_left_in_semester(username, password).get('data')

    if meal_points > 0 and days > 0:
        meal_points_per_day = meal_points / days
        return {'data': meal_points_per_day}
    elif meal_points == 0 or days == 0:
        meal_points_per_day = 0
        return {'data': meal_points_per_day}
    else:
        raise ValueError(ERROR_MESSAGE['NOT_FOUND'], httplib.NOT_FOUND)
