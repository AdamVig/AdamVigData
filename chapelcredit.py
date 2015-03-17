import newrelic.agent
newrelic.agent.initialize('./newrelic.ini')

import json, os, requests, base64, mechanize
from bs4 import BeautifulSoup
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

# Login to My.Gordon.edu with given credentials
# Returns browser instance
def loginMyGordon(username, password, browser):
    browser.open("https://my.gordon.edu/ics")

    browser.select_form(name="MAINFORM")
    browser['userName'] = username
    browser['password'] = password
    browser.submit()

    return browser

# Get meal points from My.Gordon.edu for given user
# Returns number of meal points
def getMealPoints(username, password, browser):
    mealPoints = {}
    invalidLogin = False

    # Login
    browser = loginMyGordon(username, password, browser)

    # Check for invalid login
    soup = BeautifulSoup(browser.response().read())
    loginMessage = soup.find(id="CP_V_lblLoginMessage")
    if loginMessage:
        if loginMessage.string == "Invalid Login":
            invalidLogin = True

    # Invalid login, cancel
    if invalidLogin:

        return app.make_response((
            "Invalid login to My Gordon.",
            401))

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
            # Parse HTML to find mealpoints
            soup = BeautifulSoup(browser.response().read())
            mainTable = soup.find_all('table')[1]
            pointsRow = mainTable.find_all('tr')[0]
            pointsCell = pointsRow.find_all('td')[1].find('span')
            mealPoints = { 'mealpoints': pointsCell.string }

        return app.make_response((
            json.dumps(mealPoints),
            browser.response().code))

# Get chapel credit from Go.Gordon.edu with given credentials
# Returns dictionary with:
#   credit   (int)   User's credits
#   required (int)   Total required credits
def getChapelCredit(username, password):
    response = requests.get(
        'https://go.gordon.edu/student/chapelcredits/viewattendance.cfm',
        auth=(username, password))
    chapelCredit = {}

    # Successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text)

        creditTable = soup.find_all('table')[8]

        creditRow = creditTable.find_all('tr')[0]
        creditCell = creditRow.find_all('td')[1]

        reqRow = creditTable.find_all('tr')[1]
        reqCell = reqRow.find_all('td')[1]

        chapelCredit = {
            'credit': int(creditCell.text),
            'required': int(reqCell.text)
        }

    return app.make_response((
        json.dumps(chapelCredit),
        response.status_code))

@app.route("/chapelcredit", methods=['GET'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def chapel_credit():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        password = base64.b64decode(password)
        return getChapelCredit(username, password)
    else:
        return app.make_response((
            "Please only use GET requests.",
            401))

@app.route("/mealpoints", methods=['GET'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def meal_points():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        password = base64.b64decode(password)
        return getMealPoints(username, password, mechanize.Browser())
    else:
        return app.make_response((
            "Please only use GET requests.",
            401))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
