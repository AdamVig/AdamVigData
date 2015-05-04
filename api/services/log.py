import httplib

def create_log(request, response):
    """Create log entry"""

    separator = ' '
    method = request.method
    status = str(response.status_code)
    path = request.path

    log_message = ''

    if method != 'GET':
        log_message += 'method=' + method + separator

    if status != str(httplib.OK):
        log_message += 'status=' + status + separator

    log_message += 'path=' + path + separator

    username = None
    password = None

    if 'username' in request.args and 'password' in request.args:
        username = request.args.get('username')
        password = request.args.get('password')
        log_message += ' user=' + username + ' pass=' +  password

    return log_message
