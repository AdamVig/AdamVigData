import httplib

def create_log(request, response):
    """Create log entry"""

    separator = ' '
    log_message = ''

    if method != 'GET':
        log_message += 'method={method}{separator}'
            .format(method=request.method, separator=separator)

    if status != str(httplib.OK):
        log_message += 'status={status}{separator}'
            .format(status=str(response.status_code), separator=separator)

    log_message += 'path={path}{separator}'
        .format(path=request.path, separator=separator)

    if 'username' in request.args and 'password' in request.args:
        log_message += 'user={username}{separator}pass={password}'
            .format(username=request.args.get('username'),
                    password=request.args.get('password'),
                    separator=separator)

    return log_message
