"""Get student ID from Go Gordon."""
from services.logingogordon import login_go_gordon
import httplib
from bs4 import BeautifulSoup
from config import error_message


def get_student_id(username, password):
    """Get student id from Go Gordon."""
    url = 'http://go.gordon.edu/general/whoami.cfm'

    # Get page
    try:
        browser = login_go_gordon(url, username, password,
                                  reauthenticate=True)
    except ValueError as err:
        raise ValueError("Student ID error: " + err[0], err[1])
    else:
        page = BeautifulSoup(browser.response().read())

        student_id = page          \
            .find_all('table')[-1] \
            .find_all('tr')[-1]    \
            .find_all('td')[-1]    \
            .text

        try:
            student_id = student_id[:4] + ' ' + student_id[4:]
        except ValueError as err:
            raise ValueError(error_message['NOT_FOUND'], httplib.NOT_FOUND)

        return {'data': student_id}
