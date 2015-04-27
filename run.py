from api import *
import newrelic.agent, sys, os, logging
from flask import jsonify
from logging import Formatter, StreamHandler
from logging.handlers import SysLogHandler

newrelic.agent.initialize('newrelic.ini')

os.environ['TZ'] = 'US/Eastern'
LOG_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'
DATE_FORMAT = "%b %d %I:%M:%S %p"
END_POINT = '/gocostudent/<version>/'

# Initialize request-level logging
streamhandler = StreamHandler(sys.stdout)
sysloghandler = SysLogHandler(address=('logs2.papertrailapp.com', 26735))
formatter = Formatter(LOG_FORMAT, DATE_FORMAT)
streamhandler.setFormatter(formatter)
sysloghandler.setFormatter(formatter)
app.logger.addHandler(sysloghandler)
app.logger.addHandler(streamhandler)
app.logger.setLevel(logging.INFO)

def get_data(getter, request_info):
    """Retrieve data
    getter : function to get data with
    request_info : contains credentials, endpoint name, and API version
    """

    # Get username and password
    try:
        credentials = services.getcredentials.get_credentials(request_info.get('args'))
    except ValueError as err:
        return app.make_response((err.message, 400))

    # Get data
    try:
        data = getter(credentials[0], credentials[1])
    except ValueError as err:
        if len(err.args) == 2:
            return app.make_response((err.args[0], err.args[1]))
        else:
            return app.make_response((err.message, 500))
    else:
        # Log usage
        services.getcouchdb.log_usage(credentials[0],
            request_info.get('endpoint'),
            request_info.get('version'))

        return jsonify(data)

@app.route(END_POINT + 'chapelcredits', methods=['GET', 'HEAD'])
def route_chapel_credits(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'chapelCredits',
            'version': version
        }
        return get_data(chapelcredits.get_chapel_credits, request_info)
    else:
        return "Chapel credits endpoint is working."

@app.route(END_POINT + 'mealpoints', methods=['GET', 'HEAD'])
def route_meal_points(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'mealPoints',
            'version': version
        }
        return get_data(mealpoints.get_meal_points, request_info)
    else:
        return "Meal points endpoint is working."

@app.route(END_POINT + 'daysleftinsemester', methods=['GET', 'HEAD'])
def route_days_left_in_semester(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'daysLeftInSemester',
            'version': version
        }
        return get_data(daysleftinsemester.get_days_left_in_semester, request_info)
    else:
        return "Days left in semester endpoint is working."

@app.route(END_POINT + 'mealpointsperday', methods=['GET', 'HEAD'])
def route_meal_points_per_day(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'mealPointsPerDay',
            'version': version
        }
        return get_data(mealpointsperday.get_meal_points_per_day, request_info)
    else:
        return "Meal points per day endpoint is working."

@app.route(END_POINT + 'createuser', methods=['GET', 'HEAD'])
def route_create_user(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request.args)
        return services.getcouchdb.create_user(credentials[0], version)
    else:
        return "Create user endpoint is working."

@app.route(END_POINT + 'appinfo', methods=['GET', 'HEAD'])
def route_app_info(version):
    app_info = services.getcouchdb.get_app_info()
    return jsonify(app_info)

@app.route(END_POINT + 'user/<username>', methods=['GET', 'HEAD'])
def route_user(version, username):
    try:
        user = services.getcouchdb.get_user(username)
    except ValueError as err:
        return app.make_response((err.args[0], err.args[1]))
    else:
        return jsonify(user)

@app.route('/<appname>/<version>', methods=['GET'])
def route_app(appname=None, version=None):
    return "The app server is running correctly for " + \
        appname + " " + \
        version + "."

@app.route('/', methods=['GET'])
def route_default():
    return "The app server is running correctly."

@app.before_request
def before_request():
    if 'gocostudent' not in request.url:
        return app.make_response(("Resource not found.", 404))

@app.after_request
def log_request(response):
    log = services.log.create_log(request, response)
    if response.status_code == 200:
        app.logger.info(log)
    else:
        app.logger.error(log)
    return response

@app.errorhandler(500)
def handle_500_error(err):
    return "500 Internal Server Error"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
