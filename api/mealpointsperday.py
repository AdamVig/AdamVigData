from mealpoints import get_meal_points
from daysleftinsemester import get_days_left_in_semester
import httplib

def get_meal_points_per_day(username, password):
    """Get meal points per day"""

    meal_points = get_meal_points(username, password).get('data')
    days = get_days_left_in_semester(username, password).get('data')

    if meal_points > 0 and days > 0:
        meal_points_per_day = meal_points / days
        return { 'data': meal_points_per_day }
    elif meal_points == 0 or days == 0:
        meal_points_per_day = 0
        return { 'data': meal_points_per_day }
    else:
        raise ValueError("Meal points per day are not available", \
            httplib.NOT_FOUND)
