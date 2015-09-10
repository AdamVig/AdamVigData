""""Get mealpoints from My Gordon."""
import mechanize
import httplib
from config import error_message
from bs4 import BeautifulSoup


def get_meal_points(username, password):
    """Get meal points from My Gordon."""
    # Login
    browser = login_my_gordon(
        username, password, mechanize.Browser())

    # Check for invalid login
    soup = BeautifulSoup(browser.response().read())
    if soup.find(id="CP_V_lblLoginMessage"):
        raise ValueError(error_message['UNAUTHORIZED'],
                         httplib.UNAUTHORIZED)

    # Navigate to mealpoints page
    browser.open('/ICS/Students/Mealpoints.jnz')

    # Parse HTML to find URL that iFrame points to
    page = BeautifulSoup(browser.response().read())

    # Test for error caused by professor accounts
    notFoundMessage = page.find('span', {"class": "notFound"})
    if notFoundMessage is not None:
        if notFoundMessage.string == "You do not have the necessary \
                permissions to view this page.":
            raise ValueError(error_message['NOT_FOUND'], httplib.NOT_FOUND)

    iframe = page.find('iframe')

    if iframe is None:
        raise ValueError(error_message['NOT_FOUND'], httplib.NOT_FOUND)

    # Navigate to page that displays mealpoints
    browser.open('https://my.gordon.edu' + iframe['src'])
    browser.open('https://my.gordon.edu/GMEX')

    if browser.response().code == httplib.OK:

        page = BeautifulSoup(browser.response().read())

        try:
            meal_points = page        \
                .find_all('table')[1] \
                .find_all('tr')[0]    \
                .find_all('td')[1]    \
                .find('span')         \
                .text
        except IndexError:
            meal_points = 0
        else:
            meal_points = parse_meal_points(meal_points)

        return {'data': meal_points}

    else:
        raise ValueError(error_message['INTERNAL_SERVER_ERROR'],
                         httplib.INTERNAL_SERVER_ERROR)


def parse_meal_points(meal_points):
    """Parse meal points string into a rounded integer."""
    # Remove dollar sign and comma
    meal_points = meal_points.strip('$')
    meal_points = meal_points.replace(',', '')

    # Convert to float
    meal_points = float(meal_points)

    # Round to nearest int
    meal_points = int(meal_points)

    return meal_points


def login_my_gordon(username, password, browser):
    """Login to My.Gordon.edu with given credentials.

    Returns browser instance
    """
    browser.open("https://my.gordon.edu/ics")

    browser.select_form(name="MAINFORM")
    browser['userName'] = username
    browser['password'] = password
    browser.submit()

    return browser
