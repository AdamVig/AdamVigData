"""Run the app and delegate incoming requests."""
from api import *
from api.services import *
from config import *
import newrelic.agent
import sys
import os
import logging
import httplib
import traceback
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
app.logger.setLevel(logging.DEBUG)


def get_credentials(request_info):
    """Get credentials from request."""
    try:
        return getcredentials.get_credentials(request_info.get('args'))
    except ValueError as err:
        print "ValueError in credentials: " + err.message
        if DEBUG:
            print traceback.format_exc()
        return app.make_response((error_message['INTERNAL_SERVER_ERROR'],
                                  httplib.BAD_REQUEST))


def prepare_data(data, request_info, shouldLog, shouldCache):
    """Prepare data for response by converting to JSON and logging."""
    if shouldLog is True:
        services.db.log_usage(get_credentials(request_info)[0],
                              request_info.get('endpoint'),
                              request_info.get('version'),
                              data,
                              shouldCache)

    # Return JSON if data is in correct format
    if isinstance(data, dict):
            return jsonify(data)

    # Raise error if data is not in correct format
    else:
        print "Error converting data to JSON in endpoint " + \
            request_info['endpoint']
        return app.make_response((error_message['INTERNAL_SERVER_ERROR'],
                                 httplib.BAD_GATEWAY))


def get_data(getter, request_info, shouldLog=True, shouldCache=True):
    """Get data using the provided getter function and request.

    getter : function to get data with
    request_info : contains credentials, endpoint name, and API version
    """
    credentials = get_credentials(request_info)

    try:
        data = getter(credentials[0], credentials[1])
    except ValueError as err:
        if len(err.args) == 2:
            return app.make_response((err.args[0], err.args[1]))
        else:
            print "ValueError in " + request_info['endpoint'] + \
                ": " + err.message
            if DEBUG:
                print traceback.format_exc()
            return app.make_response((error_message['INTERNAL_SERVER_ERROR'],
                                      httplib.INTERNAL_SERVER_ERROR))
    except Exception as err:
        print "Exception in " + request_info['endpoint'] + ": " + err.message
        if DEBUG:
            print traceback.format_exc()
        return app.make_response((error_message['INTERNAL_SERVER_ERROR'],
                                  httplib.INTERNAL_SERVER_ERROR))
    else:
        return prepare_data(data, request_info, shouldLog, shouldCache)


@app.route(END_POINT_PREFIX + 'chapelcredits', methods=['GET', 'POST', 'HEAD'])
def route_chapel_credits(version):
    """Handle requests for chapel credits."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'chapelCredits',
            'version': version
        }
        return get_data(get_chapel_credits, request_info)
    else:
        return "Chapel credits endpoint is working."


@app.route(END_POINT_PREFIX + 'mealpoints', methods=['GET', 'POST', 'HEAD'])
def route_meal_points(version):
    """Handle requests for meal points."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'mealPoints',
            'version': version
        }
        return get_data(get_meal_points, request_info)
    else:
        return "Meal points endpoint is working."


@app.route(END_POINT_PREFIX + 'daysleftinsemester',
           methods=['GET', 'POST', 'HEAD'])
def route_days_left_in_semester(version):
    """Handle requests for days left in semester."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'daysLeftInSemester',
            'version': version
        }
        return get_data(get_days_left_in_semester, request_info,
                        shouldCache=False)
    else:
        return "Days left in semester endpoint is working."


@app.route(END_POINT_PREFIX + 'mealpointsperday',
           methods=['GET', 'POST', 'HEAD'])
def route_meal_points_per_day(version):
    """Handle requests for meal points per day."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'mealPointsPerDay',
            'version': version
        }
        return get_data(get_meal_points_per_day, request_info)
    else:
        return "Meal points per day endpoint is working."


@app.route(END_POINT_PREFIX + 'studentid', methods=['GET', 'POST', 'HEAD'])
def route_student_id(version):
    """Handle requests for student ID."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'studentID',
            'version': version
        }
        return get_data(get_student_id, request_info, shouldCache=False)
    else:
        return "Student ID endpoint is working."


@app.route(END_POINT_PREFIX + 'studentinfo', methods=['GET', 'POST', 'HEAD'])
def route_student_info(version):
    """Handle requests for student info."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'studentInfo',
            'version': version
        }
        return get_data(get_student_info, request_info, shouldCache=False)
    else:
        return "Student info endpoint is working."


@app.route(END_POINT_PREFIX + 'nextmeal', methods=['GET', 'POST', 'HEAD'])
def route_next_meal(version):
    """Handle requests for next meal."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'nextMeal',
            'version': version
        }
        return get_data(get_next_meal, request_info, shouldCache=False)
    else:
        return "Next meal endpoint is working."


@app.route(END_POINT_PREFIX + 'temperature', methods=['GET', 'POST', 'HEAD'])
def route_temperature(version):
    """Handle requests for temperature."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'temperature',
            'version': version
        }
        return get_data(get_temperature, request_info, shouldCache=False)
    else:
        return "Temperature endpoint is working."


@app.route(END_POINT_PREFIX + 'highlandexpress',
           methods=['GET', 'POST', 'HEAD'])
def route_highland_express(version):
    """Handle requests for Highland Express data."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'highlandExpress',
            'version': version
        }
        return get_data(get_highland_express, request_info, shouldCache=True)
    else:
        return "Highland express endpoint is working."


@app.route(END_POINT_PREFIX + 'chapelevents',
           methods=['GET', 'POST', 'HEAD'])
def route_chapel_events(version):
    """Handle requests for chapel events."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'chapelEvents',
            'version': version
        }
        return get_data(get_chapel_events, request_info, shouldCache=False)
    else:
        return "Chapel events endpoint is working."


@app.route(END_POINT_PREFIX + 'nextchapelevent',
           methods=['GET', 'POST', 'HEAD'])
def route_next_chapel_event(version):
    """Handle requests for next chapel event."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'nextChapelEvent',
            'version': version
        }
        return get_data(get_next_chapel_event, request_info, shouldCache=False)
    else:
        return "Next chapel event endpoint is working."


@app.route(END_POINT_PREFIX + 'checklogin', methods=['GET', 'POST', 'HEAD'])
def route_check_login(version):
    """Handle requests to check login."""
    if request.data or request.args:
        request_info = {
            'args': request.args or request.get_json(),
            'endpoint': 'checkLogin',
            'version': version
        }
        return get_data(check_login, request_info, shouldLog=False,
                        shouldCache=False)
    else:
        return "Check login endpoint is working."


@app.route(END_POINT_PREFIX + 'setproperty', methods=['GET', 'POST', 'HEAD'])
def route_set_property(version):
    """Handle requests to set a property in user data."""
    if request.data or request.args:
        params = request.args or request.get_json()
        credentials = services.getcredentials.get_credentials(params)
        property_name = request.args.get('property')
        value = request.args.get('value')
        try:
            user = db.set_property(credentials[0], property_name, value)
        except ValueError as err:
            if len(err.args) == 2:
                return app.make_response((err.args[0], err.args[1]))
            else:
                return app.make_response((err.message,
                                         httplib.INTERNAL_SERVER_ERROR))
        else:
            return jsonify(user)
    else:
        return "Set property endpoint is working."


@app.route(END_POINT_PREFIX + 'createuser', methods=['GET', 'POST', 'HEAD'])
def route_create_user(version):
    """Create a new user doc in the database."""
    if request.data or request.args:
        params = request.args or request.get_json()
        credentials = services.getcredentials.get_credentials(params)
        try:
            user = services.db.create_user(credentials[0], version)
        except ValueError as err:
            if len(err.args) == 2:
                return app.make_response((err.args[0], err.args[1]))
            else:
                return app.make_response((err.message,
                                         httplib.INTERNAL_SERVER_ERROR))
        else:
            return jsonify(user)
    else:
        return "Create user endpoint is working."


@app.route(END_POINT_PREFIX + 'appinfo', methods=['GET', 'POST', 'HEAD'])
def route_app_info(version):
    """Handle requests for app info."""
    app_info = services.db.get_doc('info')
    return jsonify(app_info)


@app.route('/<appname>/<version>', methods=['GET'])
def route_app(appname=None, version=None):
    """Report app name and version."""
    return "The app server is running correctly for " + \
        appname + " " + \
        version + "."


@app.route('/', methods=['GET'])
def route_default():
    """Report generic server status."""
    return "The app server is running correctly."


@app.before_request
def before_request():
    """Decline any requests that are not for gocostudent resources."""
    if 'gocostudent' not in request.url:
        return app.make_response(("Resource not found.", httplib.NOT_FOUND))


@app.after_request
def after_request(response):
    """Log request in application logger."""
    log = services.log.create_log(request, response)
    if response.status_code == httplib.OK:
        app.logger.info(log)
    else:
        app.logger.error(log)

    # Add CORS headers to response
    response.headers['Access-Control-Allow-Origin'] = \
        request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    response.headers['Access-Control-Allow-Headers'] = \
        request.headers.get('Access-Control-Request-Headers',
                            'Authorization')
    return response


@app.errorhandler(httplib.INTERNAL_SERVER_ERROR)
def handle_500_error(err):
    """Return generic error message for internal server error."""
    return app.make_response((error_message['INTERNAL_SERVER_ERROR'],
                             httplib.INTERNAL_SERVER_ERROR))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
