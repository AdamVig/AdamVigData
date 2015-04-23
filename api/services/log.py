def create_log(request, response):
    """Create log entry"""

    return 'method=' + request.method + \
        ' status=' + str(response.status_code) + \
        ' path=' + request.path + \
        ' user=' + request.args.get('username') + \
        ' pass=' + request.args.get('password')
