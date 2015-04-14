import mealpoints, daysleftinsemester

def get_meal_points_per_day(username, password):
    """Get meal points per day"""

    meal_points = mealpoints.get_meal_points(username, password)[0]['data']
    days = daysleftinsemester.get_days_left_in_semester()[0]['data']

    if meal_points > 0 and days > 0:
        num_digits = 2
        meal_points_per_day = round(meal_points / days, num_digits)
        return { 'data': meal_points_per_day }, 200

    elif meal_points == 0 or days == 0:
        meal_points_per_day = 0
        return { 'data': meal_points_per_day }, 200

    else:
        return "Meal points per day are not available", \
            browser.response().code