from api import *
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

end_point = '/gocostudent/<version>/'

@app.route(end_point + 'chapelcredits', methods=['GET', 'HEAD'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_chapel_credits(version):
    if request.method == 'GET':
        credentials = services.getcredentials.get_credentials(request)
        services.getcouchdb.log_usage(credentials[0], 'chapelCredits')
        data = chapelcredits.get_chapel_credits(credentials[0], credentials[1])
        return app.make_response((json.dumps(data[0]), data[1]))
    else:
        return "Chapel credits endpoint is working."

@app.route(end_point + 'mealpoints', methods=['GET', 'HEAD'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_meal_points(version):
    if request.method == 'GET':
        credentials = services.getcredentials.get_credentials(request)
        services.getcouchdb.log_usage(credentials[0], 'mealPoints')
        data = mealpoints.get_meal_points(credentials[0], credentials[1])
        return app.make_response((json.dumps(data[0]), data[1]))
    else:
        return "Meal points endpoint is working."

@app.route(end_point + 'daysleftinsemester', methods=['GET', 'HEAD'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_days_left_in_semester(version):
    if request.method == 'GET':
        credentials = services.getcredentials.get_credentials(request)
        data = daysleftinsemester.get_days_left_in_semester()
        services.getcouchdb.log_usage(credentials[0], 'daysLeftInSemester')
        return app.make_response((json.dumps(data[0]), data[1]))
    else:
        return "Days left in semester endpoint is working."

@app.route(end_point + 'mealpointsperday', methods=['GET', 'HEAD'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_meal_points_per_day(version):
    credentials = services.getcredentials.get_credentials(request)
    services.getcouchdb.log_usage(credentials[0], 'mealPointsPerDay')
    if request.method == 'GET':
        data = mealpointsperday.get_meal_points_per_day(
            credentials[0],
            credentials[1])
        return app.make_response((json.dumps(data[0]), data[1]))
    else:
        return "Meal points per day endpoint is working."

@app.route(end_point + 'appinfo', methods=['GET', 'HEAD'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_app_info(version):
    app_info = services.getcouchdb.get_app_info()
    return json.dumps(app_info)

@app.route(end_point + 'user/<username>/', methods=['GET', 'HEAD'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_user(version, username):
    user = services.getcouchdb.get_user(username)
    return json.dumps(user)

@app.route('/<appname>/<version>/', methods=['GET'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_app(appname=None, version=None):
    return "The app server is running correctly for " + \
        appname + " " + \
        version + "."

@app.route('/', methods=['GET'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def route_default():
    return "The app server is running correctly."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
