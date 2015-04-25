import mechanize, urllib2
from bs4 import BeautifulSoup

def get_chapel_credits(username, password):
    """Get chapel credits from Go Gordon"""

    # Retrieve page
    url = 'https://go.gordon.edu/student/chapelcredits/viewattendance.cfm'
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.add_password(url, username, password)

    try:
        browser.open(url)

    except urllib2.HTTPError as err:
        if err.code == 401:
            raise ValueError("Username and password do not match.", 401)
        else:
            raise ValueError("HTTPError: Chapel credits are unavailable.", 500)

    except Exception as err:
        raise ValueError("Chapel credits are unavailable.", 500)

    else:
        response = browser.response().read()

    if "No Christian Life and Worship Credit Found" in response:
        raise ValueError("No chapel credits found.", 404)

    # Find chapel credits on page
    page = BeautifulSoup(response)

    credit_table = page.find_all('table')[8]

    credits = credit_table \
        .find_all('tr')[0] \
        .find_all('td')[1] \
        .text

    required = credit_table \
        .find_all('tr')[1]  \
        .find_all('td')[1]  \
        .text

    return {
        'data': int(credits),
        'outof': int(required)
    }
