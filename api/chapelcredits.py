"""Get chapel credits from Go Gordon."""
from services.logingogordon import login_go_gordon
from config import ERROR_INFO
import httplib
from bs4 import BeautifulSoup


def get_chapel_credits(username, password):
    """Get chapel credits from Go Gordon."""
    # Retrieve page
    url = 'https://go.gordon.edu/student/chapelcredits/viewattendance.cfm'

    try:
        browser = login_go_gordon(url, username, password,
                                  reauthenticate=False)
    except ValueError as err:
        raise ValueError(err[0], err[1])
    else:
        response = browser.response().read()

    if "No Christian Life and Worship Credit Found" in response:
        return {
            'data': 0,
            'outof': 0
        }

    # Find chapel credits on page
    page = BeautifulSoup(response)

    try:
        credit_table = page.find_all('table')[8]
    except IndexError as err:
        print err
        raise ValueError(ERROR_INFO['NOT_FOUND'])
    else:
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
