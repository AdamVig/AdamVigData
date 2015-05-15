import httplib, requests, services

def check_login(username, password):
    """Check login on Go Gordon"""

    url = 'https://go.gordon.edu/'
    auth = username + ':' + password + '@'

    try:
        response = requests.head(url, auth=(username, password))

    except requests.exceptions.RequestException as e:
        raise ValueError("Unexpected error.", httplib.INTERNAL_SERVER_ERROR)

    else:
        if response.status_code == httplib.OK:
            try:
                user = services.db.get_user(username)
            except ValueError as err:
                print "Valid login but user does not exist in database."
            else:
                return { 'data': user }


        elif response.status_code == httplib.UNAUTHORIZED:
            raise ValueError("Invalid login.", httplib.UNAUTHORIZED)

        else:
            raise ValueError("Unexpected error.", httplib.INTERNAL_SERVER_ERROR)
