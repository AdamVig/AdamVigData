"""Log user in to Go Gordon."""
import mechanize
import httplib
import urllib2
import config


def login_go_gordon(url, username, password, reauthenticate=False):
    """Login to Go Gordon and return an instance of Mechanize browser.

    reauthenticate parameter dictates whether or not to pass the browser
    through the /level3logon page which allows access to private student info
    """
    reauth_url = 'http://go.gordon.edu/lib/auth/level3logon.cfm'

    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.add_password(url, username, password)

    if reauthenticate is True:
        browser.add_password(reauth_url, username, password)

    try:
        browser.open(url)
    except urllib2.HTTPError as err:
        if err.code == httplib.UNAUTHORIZED:
            raise ValueError(config.error_message['UNAUTHORIZED'],
                             httplib.UNAUTHORIZED)
        else:
            raise ValueError(config.error_message['INTERNAL_SERVER_ERROR'],
                             httplib.INTERNAL_SERVER_ERROR)

    except Exception as err:
        raise ValueError(config.error_message['INTERNAL_SERVER_ERROR'],
                         httplib.INTERNAL_SERVER_ERROR)
    else:

        if reauthenticate is True:
            # Submit authentication form
            browser.select_form(name="form1")
            browser['password'] = password
            browser.submit()

            error_message = "Logon failure: unknown user name or bad password"

            if error_message in browser.response().read():
                raise ValueError(config.error_message['UNAUTHORIZED'],
                                 httplib.UNAUTHORIZED)

        return browser
