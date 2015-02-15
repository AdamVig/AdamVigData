import mechanize, json
from bs4 import BeautifulSoup
from collections import OrderedDict
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

# Get dining menu from Go.Gordon.edu with given credentials
# Returns dictionary with:
#   'DAY': (MON, TUE, WED, etc.)
#       'breakfast'    (string)    Breakfast menu
#       'lunch'        (string)    Lunch menu
#       'dinner'       (string)    Dinner menu
#   'DAY':
#       ... (see above)
def getDiningMenu(username, password, browser):
    browser = loginGoGordon(username, password, browser)
    browser.open("https://go.gordon.edu/departments/dining/menu.cfm")

    soup = BeautifulSoup(browser.response().read())

    tables = soup.find_all('table')
    nestedTables = tables[0].find_all('table')
    menuTable = nestedTables[5]
    days = menuTable.find_all('tr')[2:]

    menu = OrderedDict()

    for day in days:
        cells = day.find_all('td')
        cells = map(lambda cell:cell.text, cells)
        menu[cells[0]] = {}
        menu[cells[0]]['breakfast'] = cells[1]
        menu[cells[0]]['lunch'] = cells[2]
        menu[cells[0]]['dinner'] = cells[3]

    return menu

def printDiningMenu(diningMenu):
    for dayName, dayMenu in diningMenu.iteritems():
        print "-------------------------------"
        print dayName, "Dinner: "
        print dayMenu["dinner"]
