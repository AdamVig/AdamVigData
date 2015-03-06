import mechanize, json
from bs4 import BeautifulSoup
from collections import OrderedDict
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

    # Login and navigate to mealpoints page
    browser = loginMyGordon(username, password, browser)
    mealpointsLink = browser.open('/ICS/Students/Mealpoints.jnz')

    # Parse HTML to find URL that iFrame points to
    soup = BeautifulSoup(browser.response().read())
    iframeSrc = soup.find('iframe')['src']

    # Navigate to page that displays mealpoints
    browser.open('https://my.gordon.edu' + iframeSrc)
    browser.open('https://my.gordon.edu/GMEX')

    # Parse HTML to find mealpoints
    soup = BeautifulSoup(browser.response().read())
    mainTable = soup.find_all('table')[1]
    pointsRow = mainTable.find_all('tr')[0]
    pointsCell = pointsRow.find_all('td')[1].find('span')
    mealPoints = pointsCell.string

    return mealPoints
