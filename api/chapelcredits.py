import mechanize
from bs4 import BeautifulSoup

def get_chapel_credits(username, password):
    """Get chapel credits from Go Gordon"""

    # Retrieve page
    url = 'https://go.gordon.edu/student/chapelcredits/viewattendance.cfm'
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.add_password(url, username, password)
    browser.open(url)

    if browser.response().code == 200:

        if not "No Christian Life and Worship Credit Found" in browser.response().read():
            page = BeautifulSoup(browser.response().read())

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
        else:
            raise ValueError("No chapel credits found.", 404)
    elif browser.response().code == 401:
        raise ValueError("Username and password do not match.", 401)
    else:
        raise ValueError("Chapel credits are unavailable.", browser.response().code)
