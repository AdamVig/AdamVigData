from api import *
from config import *
import newrelic.agent, sys, os, logging, httplib
from flask import jsonify
from logging import Formatter, StreamHandler
from logging.handlers import SysLogHandler

if not app.config.get('TESTING'):
    newrelic.agent.initialize('newrelic.ini')
os.environ['TZ'] = 'US/Eastern'

# Initialize logging
streamhandler = StreamHandler(sys.stdout)
sysloghandler = SysLogHandler(address=(PAPERTRAIL_URL, PAPERTRAIL_PORT))
formatter = Formatter(LOG_FORMAT)
streamhandler.setFormatter(formatter)
sysloghandler.setFormatter(formatter)
app.logger.addHandler(sysloghandler)
app.logger.addHandler(streamhandler)
app.logger.setLevel(logging.INFO)

def get_data(getter, request_info, log=True):
    """Retrieve data
    getter : function to get data with
    request_info : contains credentials, endpoint name, and API version
    """

    # Get username and password
    try:
        credentials = services.getcredentials.get_credentials(request_info.get('args'))
    except ValueError as err:
        return app.make_response((err.message, httplib.BAD_REQUEST))

    # Get data
    try:
        data = getter(credentials[0], credentials[1])
    except ValueError as err:
        if len(err.args) == 2:
            return app.make_response((err.args[0], err.args[1]))
        else:
            return app.make_response((err.message, httplib.INTERNAL_SERVER_ERROR))
    else:
        if log == True:
            # Log usage
            services.db.log_usage(credentials[0],
                request_info.get('endpoint'),
                request_info.get('version'),
                data)

        return jsonify(data)

@app.route(END_POINT_PREFIX + 'chapelcredits', methods=['GET', 'HEAD'])
def route_chapel_credits(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'chapelCredits',
            'version': version
        }
        return get_data(get_chapel_credits, request_info)
    else:
        return "Chapel credits endpoint is working."

@app.route(END_POINT_PREFIX + 'mealpoints', methods=['GET', 'HEAD'])
def route_meal_points(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'mealPoints',
            'version': version
        }
        return get_data(get_meal_points, request_info)
    else:
        return "Meal points endpoint is working."

@app.route(END_POINT_PREFIX + 'daysleftinsemester', methods=['GET', 'HEAD'])
def route_days_left_in_semester(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'daysLeftInSemester',
            'version': version
        }
        return get_data(get_days_left_in_semester, request_info)
    else:
        return "Days left in semester endpoint is working."

@app.route(END_POINT_PREFIX + 'mealpointsperday', methods=['GET', 'HEAD'])
def route_meal_points_per_day(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'mealPointsPerDay',
            'version': version
        }
        return get_data(get_meal_points_per_day, request_info)
    else:
        return "Meal points per day endpoint is working."

@app.route(END_POINT_PREFIX + 'studentid', methods=['GET', 'HEAD'])
def route_student_id(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'studentID',
            'version': version
        }
        return get_data(get_student_id, request_info)
    else:
        return "Student ID endpoint is working."

@app.route(END_POINT_PREFIX + 'nextmeal', methods=['GET', 'HEAD'])
def route_next_meal(version):
    if request.method == 'GET' and request.args:
        request_info = {
            'args': request.args,
            'endpoint': 'nextMeal',
            'version': version
        }
        return get_data(get_next_meal, request_info)
    else:
        return "Next meal endpoint is working."

@app.route(END_POINT_PREFIX + 'checklogin', methods=['GET', 'HEAD'])
def route_check_login(version):
    if request.method == 'GET' and request.args:
        # Get username and password
        try:
            credentials = services.getcredentials.get_credentials(request.args)
        except ValueError as err:
            return app.make_response((err.message, httplib.BAD_REQUEST))

        # Get data
        try:
            data = check_login(credentials[0], credentials[1])

        # Invalid login or unknown error
        except ValueError as err:
            if len(err.args) == 2:
                return app.make_response((err.args[0], err.args[1]))
            else:
                return app.make_response((err.message, httplib.INTERNAL_SERVER_ERROR))
        else:
            return jsonify(data)
    else:
        return "Check login endpoint is working."

@app.route(END_POINT_PREFIX + 'createuser', methods=['GET', 'HEAD'])
def route_create_user(version):
    if request.method == 'GET' and request.args:
        credentials = services.getcredentials.get_credentials(request.args)
        return services.db.create_user(credentials[0], version)
    else:
        return "Create user endpoint is working."

@app.route(END_POINT_PREFIX + 'appinfo', methods=['GET', 'HEAD'])
def route_app_info(version):
    app_info = services.db.get_app_info()
    return jsonify(app_info)

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
        return app.make_response(("Resource not found.", httplib.NOT_FOUND))

@app.after_request
def log_request(response):
    log = services.log.create_log(request, response)
    if response.status_code == httplib.OK:
        app.logger.info(log)
    else:
        app.logger.error(log)
    return response

@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def handle_500_error(err):
    return "500 Internal Server Error"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
