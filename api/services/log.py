"""Create an HTTP log entry."""
import httplib


def create_log(request, response):
    """Create an HTTP log entry based on a request and response."""
    separator = ' '
    log_message = ''
    method = request.method
    status = str(response.status_code)
    request_data = request.args or request.get_json()
    response_data = response.data
    path = request.path

    if method != 'GET' and method != 'POST':
        log_message += 'method={method}{separator}' \
            .format(method=method, separator=separator)

    if status != str(httplib.OK):
        log_message += 'status={status}{separator}' \
            .format(status=status, separator=separator)
        log_message += 'error={error}{separator}' \
            .format(error=response_data, separator=separator)

    log_message += 'path={path}{separator}' \
        .format(path=path, separator=separator)

    if 'username' in request_data:
        log_message += 'user={username}{separator}' \
            .format(username=request_data.get('username'),
                    separator=separator)

    return log_message
