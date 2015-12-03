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
            raise ValueError(config.ERROR_INFO['UNAUTHORIZED'])
        else:
            raise ValueError(config.ERROR_INFO['INTERNAL_SERVER_ERROR'])

    except Exception as err:
        raise ValueError(config.ERROR_INFO['INTERNAL_SERVER_ERROR'])
    else:

        if reauthenticate is True:

            try:
                browser.select_form(name="form1")
            except mechanize.FormNotFoundError:
                pass
            else:
                browser['password'] = password
                browser.submit()

            page_error = "Logon failure: unknown user name or bad password"

            if page_error in browser.response().read():
                raise ValueError(config.ERROR_INFO['UNAUTHORIZED'])

        return browser
