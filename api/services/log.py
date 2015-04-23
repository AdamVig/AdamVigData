def create_log(request, response):
    """Create log entry"""

    method = request.method
    status = str(response.status_code)
    path = request.path

    log_message = 'method=' + method + \
        ' status=' + status + \
        ' path=' + path

    username = None
    password = None

    if 'username' in request.args and 'password' in request.args:
        username = request.args.get('username')
        password = request.args.get('password')
        log_message += ' user=' + username + ' pass=' +  password

    return log_message
