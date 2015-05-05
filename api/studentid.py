import requests, json, mechanize, httplib, urllib2
from bs4 import BeautifulSoup

def get_student_id(username, password):
    """Get student id from Go Gordon"""

    auth_url = 'http://go.gordon.edu/lib/auth/level3logon.cfm'
    whoami_url = 'http://go.gordon.edu/general/whoami.cfm'

    # Initialize browser
    browser = mechanize.Browser()
    browser.set_handle_robots(False)

    # Add page authentication
    browser.add_password(whoami_url, username, password)
    browser.add_password(auth_url, username, password)

    # Get page
    try:
        browser.open(whoami_url)
    except urllib2.HTTPError as err:
        if err.code == httplib.UNAUTHORIZED:
            raise ValueError("Username and password do not match.",
                httplib.UNAUTHORIZED)
        else:
            raise ValueError("HTTPError: Student ID is unavailable.",
                httplib.INTERNAL_SERVER_ERROR)

    except Exception as err:
        raise ValueError("Student ID is unavailable.",
            httplib.INTERNAL_SERVER_ERROR)

    # Submit authentication form
    browser.select_form(name="form1")
    browser['password'] = password
    browser.submit()

    if browser.response().code == httplib.OK:
        page = BeautifulSoup(browser.response().read())

        student_id = page          \
            .find_all('table')[-1] \
            .find_all('tr')[-1]    \
            .find_all('td')[-1]    \
            .text

        return { 'data': student_id }

    else:
        return response.status_code
