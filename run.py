from api import *
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

end_point = '/gocostudent/<version>/'

@app.route(end_point + 'chapelcredits', methods=['GET', 'HEAD'])
def route_chapel_credits(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request)
        services.getcouchdb.log_usage(credentials[0], 'chapelCredits', version)
        data = chapelcredits.get_chapel_credits(credentials[0], credentials[1])
        if isinstance(data[0], dict):
            return app.make_response((json.dumps(data[0]), data[1]))
        else:
            return app.make_response((data[0], data[1]))
    else:
        return "Chapel credits endpoint is working."

@app.route(end_point + 'mealpoints', methods=['GET', 'HEAD'])
def route_meal_points(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request)
        services.getcouchdb.log_usage(credentials[0], 'mealPoints', version)
        data = mealpoints.get_meal_points(credentials[0], credentials[1])
        if isinstance(data[0], dict):
            return app.make_response((json.dumps(data[0]), data[1]))
        else:
            return app.make_response((data[0], data[1]))
    else:
        return "Meal points endpoint is working."

@app.route(end_point + 'daysleftinsemester', methods=['GET', 'HEAD'])
def route_days_left_in_semester(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request)
        data = daysleftinsemester.get_days_left_in_semester()
        services.getcouchdb.log_usage(credentials[0], 'daysLeftInSemester', version)
        if isinstance(data[0], dict):
            return app.make_response((json.dumps(data[0]), data[1]))
        else:
            return app.make_response((data[0], data[1]))
    else:
        return "Days left in semester endpoint is working."

@app.route(end_point + 'mealpointsperday', methods=['GET', 'HEAD'])
def route_meal_points_per_day(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request)
        services.getcouchdb.log_usage(credentials[0], 'mealPointsPerDay', version)
        data = mealpointsperday.get_meal_points_per_day(
            credentials[0],
            credentials[1])
        if isinstance(data[0], dict):
            return app.make_response((json.dumps(data[0]), data[1]))
        else:
            return app.make_response((data[0], data[1]))
    else:
        return "Meal points per day endpoint is working."

@app.route(end_point + 'appinfo', methods=['GET', 'HEAD'])
def route_app_info(version):
    app_info = services.getcouchdb.get_app_info()
    return json.dumps(app_info)

@app.route(end_point + 'user/<username>/', methods=['GET', 'HEAD'])
def route_user(version, username):
    user = services.getcouchdb.get_user(username)
    if isinstance(user, dict):
        return json.dumps(user)
    else:
        return user

@app.route('/<appname>/<version>/', methods=['GET'])
def route_app(appname=None, version=None):
    return "The app server is running correctly for " + \
        appname + " " + \
        version + "."

@app.route('/', methods=['GET'])
def route_default():
    return "The app server is running correctly."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
