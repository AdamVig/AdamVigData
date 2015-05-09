import mechanize, httplib, urllib2

def login_go_gordon(url, username, password, reauthenticate=False):
    """Login to Go Gordon, return an instance of Mechanize browser"""

    reauth_url = 'http://go.gordon.edu/lib/auth/level3logon.cfm'

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.add_password(url, username, password)

    if reauthenticate == True:
        browser.add_password(reauth_url, username, password)

    try:
        browser.open(url)
    except urllib2.HTTPError as err:
        if err.code == httplib.UNAUTHORIZED:
            raise ValueError("Username and password do not match.",
                httplib.UNAUTHORIZED)
        else:
            raise ValueError("HTTPError: Login failed.",
                httplib.INTERNAL_SERVER_ERROR)

    except Exception as err:
        raise ValueError("Login failed.",
            httplib.INTERNAL_SERVER_ERROR)
    else:

        if reauthenticate == True:
            # Submit authentication form
            browser.select_form(name="form1")
            browser['password'] = password
            browser.submit()

            error_message = "Logon failure: unknown user name or bad password"

            if error_message in browser.response().read():
                raise ValueError("Invalid login.", httplib.UNAUTHORIZED)

        return browser
