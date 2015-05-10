import mechanize, urllib2, httplib, services

def check_login(username, password):
    """Check login on Go Gordon"""

    # Retrieve page
    url = 'https://go.gordon.edu/'
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.add_password(url, username, password)

    try:
        browser.open(url)

    except urllib2.HTTPError as err:
        if err.code == httplib.UNAUTHORIZED:
            raise ValueError("Invalid login.",
                httplib.UNAUTHORIZED)
        else:
            raise ValueError("HTTPError: Unexpected error.",
                httplib.INTERNAL_SERVER_ERROR)

    except Exception as err:
        raise ValueError("Unexpected error.",
            httplib.INTERNAL_SERVER_ERROR)

    else:
        try:
            user = services.db.get_user(username)
        except ValueError as err:
            return "Valid login but user does not exist in database."
        else:
            return { 'data': user }
