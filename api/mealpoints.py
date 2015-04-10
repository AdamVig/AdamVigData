import requests, json, mechanize
from services import loginmygordon
from bs4 import BeautifulSoup

def get_meal_points(username, password):
    """Get meal points from My Gordon"""

    url = 'go.gordon.edu/student/chapelcredits/viewattendance.cfm'
    response = requests.get('https://' + username + ':' + password + '@' + url)

    invalid_login = False

    # Login
    browser = loginmygordon.login_my_gordon(
        username, password, mechanize.Browser())

    # Check for invalid login
    soup = BeautifulSoup(browser.response().read())
    loginMessage = soup.find(id="CP_V_lblLoginMessage")
    if loginMessage:
        if loginMessage.string == "Invalid Login":
            invalid_login = True

    # Invalid login, cancel
    if invalid_login:

        return "Invalid login to My Gordon.", 401

    # Valid login, proceed
    else:

        # Navigate to mealpoints page
        browser.open('/ICS/Students/Mealpoints.jnz')

        # Parse HTML to find URL that iFrame points to
        page = BeautifulSoup(browser.response().read())
        iframe_src = page.find('iframe')['src']

        # Navigate to page that displays mealpoints
        browser.open('https://my.gordon.edu' + iframe_src)
        browser.open('https://my.gordon.edu/GMEX')

        if browser.response().code == 200:

            page = BeautifulSoup(browser.response().read())

            meal_points = page        \
                .find_all('table')[1] \
                .find_all('tr')[0]    \
                .find_all('td')[1]    \
                .find('span')         \
                .text

            meal_points = parse_meal_points(meal_points)

            return { 'data': meal_points }, 200

        else:
            return "Meal points are not available", browser.response().code

def parse_meal_points(meal_points):
    """Parses meal points string into a rounded integer"""

    # Remove dollar sign
    meal_points = meal_points[1:]

    # Convert to float
    meal_points = float(meal_points)

    # Round
    num_digits = 2
    meal_points = round(meal_points, num_digits)

    return meal_points
