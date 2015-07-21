"""Get basic student info from Go Gordon."""
from services.logingogordon import login_go_gordon
from bs4 import BeautifulSoup


def get_student_info(username, password):
    """Get basic student info from Go Gordon."""
    url = 'http://go.gordon.edu/general/whoami.cfm'

    try:
        browser = login_go_gordon(url, username, password, reauthenticate=True)
    except ValueError as err:
        raise ValueError("Student info error: " + err[0], err[1])
    else:
        page = BeautifulSoup(browser.response().read())

        student_name = page        \
            .find_all('table')[-1] \
            .find_all('tr')[0]     \
            .find_all('td')[-1]    \
            .text

        student_email = page       \
            .find_all('table')[-1] \
            .find_all('tr')[1]     \
            .find_all('td')[-1]    \
            .text

        student_barcode = page     \
            .find_all('table')[-1] \
            .find_all('tr')[2]     \
            .find_all('td')[-1]    \
            .text

        student_id = page          \
            .find_all('table')[-1] \
            .find_all('tr')[3]     \
            .find_all('td')[-1]    \
            .text

        student_description = "{name} \r\n{email} \r\nID: {id} \r\n \
            Barcode: {barcode}" \
            .format(name=student_name,
                    email=student_email,
                    id=student_id,
                    barcode=student_barcode)

        return {
            'data': student_description,
            'name': student_name,
            'email': student_email,
            'barcode': int(student_barcode),
            'id': int(student_id)
        }
