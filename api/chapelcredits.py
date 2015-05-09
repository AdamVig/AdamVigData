import services, mechanize, httplib
from bs4 import BeautifulSoup

def get_chapel_credits(username, password):
    """Get chapel credits from Go Gordon"""

    # Retrieve page
    url = 'https://go.gordon.edu/student/chapelcredits/viewattendance.cfm'

    try:
        browser = services.logingogordon.login_go_gordon(url,
            username,
            password,
            reauthenticate=False)
    except ValueError as err:
        raise ValueError("Chapel credits error: " + err[0], err[1])
    else:
        response = browser.response().read()

    if "No Christian Life and Worship Credit Found" in response:
        raise ValueError("No chapel credits found.", httplib.NOT_FOUND)

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
