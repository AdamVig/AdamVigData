import requests, json, mechanize
from services import loginmygordon
from bs4 import BeautifulSoup

def get_meal_points(username, password):
    """Get meal points from My Gordon"""

    url = 'go.gordon.edu/student/chapelcredits/viewattendance.cfm'
    response = requests.get('https://' + username + ':' + password + '@' + url)

    mealPoints = {}
    invalidLogin = False

    # Login
    browser = loginmygordon.login_my_gordon(
        username, password, mechanize.Browser())

    # Check for invalid login
    soup = BeautifulSoup(browser.response().read())
    loginMessage = soup.find(id="CP_V_lblLoginMessage")
    if loginMessage:
        if loginMessage.string == "Invalid Login":
            invalidLogin = True

    # Invalid login, cancel
    if invalidLogin:

        return "Invalid login to My Gordon.", 401

    # Valid login, proceed
    else:

        # Navigate to mealpoints page
        browser.open('/ICS/Students/Mealpoints.jnz')

        # Parse HTML to find URL that iFrame points to
        soup = BeautifulSoup(browser.response().read())
        iframe = soup.find('iframe')
        iframeSrc = iframe['src']

        # Navigate to page that displays mealpoints
        browser.open('https://my.gordon.edu' + iframeSrc)
        browser.open('https://my.gordon.edu/GMEX')

        if browser.response().code == 200:

            page = BeautifulSoup(browser.response().read())

            meal_points = page        \
                .find_all('table')[1] \
                .find_all('tr')[0]    \
                .find_all('td')[1]    \
                .find('span')         \
                .text

            return { 'data': meal_points }, 200

        else:
            return "Meal points are not available", browser.response().code
