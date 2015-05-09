import services, mechanize, httplib
from bs4 import BeautifulSoup

def get_student_id(username, password):
    """Get student id from Go Gordon"""

    url = 'http://go.gordon.edu/general/whoami.cfm'

    # Get page
    try:
        browser = services.logingogordon.login_go_gordon(url,
            username,
            password,
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
            student_id = int(student_id)
        except ValueError as err:
            raise ValueError("Could not find student ID.", httplib.NOT_FOUND)

        return { 'data': student_id }
