from api import *
import newrelic.agent, logging, sys, os

newrelic.agent.initialize('newrelic.ini')

os.environ['TZ'] = 'US/Eastern'
LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
DATE_FORMAT = "%b %d %H:%M:%S %p"
END_POINT = '/gocostudent/<version>/'

# Initialize request-level logging
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route(END_POINT + 'chapelcredits', methods=['GET', 'HEAD'])
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

@app.route(END_POINT + 'mealpoints', methods=['GET', 'HEAD'])
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

@app.route(END_POINT + 'daysleftinsemester', methods=['GET', 'HEAD'])
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

@app.route(END_POINT + 'mealpointsperday', methods=['GET', 'HEAD'])
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

@app.route(END_POINT + 'createuser', methods=['GET', 'HEAD'])
def route_create_user(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request)
        return services.getcouchdb.create_user(credentials[0], version)
    else:
        return "Create user endpoint is working."

@app.route(END_POINT + 'appinfo', methods=['GET', 'HEAD'])
def route_app_info(version):
    app_info = services.getcouchdb.get_app_info()
    return json.dumps(app_info)

@app.route(END_POINT + 'user/<username>/', methods=['GET', 'HEAD'])
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

@app.after_request
def log_request(response):
    log = services.log.create_log(request, response)
    if response.status_code == 200:
        app.logger.info(log)
    else:
        app.logger.exception(log)
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
