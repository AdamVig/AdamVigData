import httplib

def create_log(request, response):
    """Create log entry"""

    separator = ' '
    log_message = ''
    method = request.method
    status = str(response.status_code)
    path = request.path

    if method != 'GET':
        log_message += 'method={method}{separator}' \
            .format(method=method, separator=separator)

    if status != str(httplib.OK):
        log_message += 'status={status}{separator}' \
            .format(status=status, separator=separator)

    log_message += 'path={path}{separator}' \
        .format(path=path, separator=separator)

    if 'username' in request.args:
        log_message += 'user={username}{separator}' \
            .format(username=request.args.get('username'), \
                    separator=separator)

    return log_message
