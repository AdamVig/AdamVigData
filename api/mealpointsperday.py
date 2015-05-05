from mealpoints import get_meal_points
from daysleftinsemester import get_days_left_in_semester

def get_meal_points_per_day(username, password):
    """Get meal points per day"""

    meal_points = get_meal_points(username, password).get('data')
    days = get_days_left_in_semester(username, password).get('data')

    if meal_points > 0 and days > 0:
        num_digits = 2
        meal_points_per_day = round(meal_points / days, num_digits)
        return { 'data': meal_points_per_day }
    elif meal_points == 0 or days == 0:
        meal_points_per_day = 0
        return { 'data': meal_points_per_day }
    else:
        raise ValueError("Meal points per day are not available", \
            browser.response().code)
