import mechanize, json
from bs4 import BeautifulSoup
from collections import OrderedDict
from flask import Flask, request

app = Flask(__name__)

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
    browser = loginMyGordon(username, password, browser)

    studentsLink = browser.find_link(url="./Students/")
    browser.follow_link(studentsLink)

    mealpointsLink = browser.find_link(url="/ICS/Students/Mealpoints.jnz")
    browser.follow_link(mealpointsLink)
    headers = [
        ('Cookie', "ASP.NET_SessionId=55zcxgufse0frq3jyzpkxj5r; _ga=GA1.2.151033858.1421028027; __utmt=1; __utma=156794413.151033858.1421028027.1422829862.1422836737.8; __utmb=156794413.10.10.1422836737; __utmc=156794413; __utmz=156794413.1421261850.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); .sessionheartbeat=2/1/2015 8:36:31 PM"),
        ('Referer', "https://my.gordon.edu/gmex/home/bounce?fwkid=deff9811-eb12-4572-8302-da42ebcf29d1")
    ]
    browser.addheaders = headers;
    browser.open("https://my.gordon.edu/GMEX")
    print browser.geturl()
    soup = BeautifulSoup(browser.response().read())
    print soup



# Login to My.Gordon.edu with given credentials
# Returns browser instance
def loginGoGordon(username, password, browser):
    browser.add_password("https://go.gordon.edu", username, password)
    return browser

# Get chapel credit from Go.Gordon.edu with given credentials
# Returns dictionary with:
#   credit   (int)   User's credits
#   required (int)   Total required credits
def getChapelCredit(username, password, browser):
    browser = loginGoGordon(username, password, browser)
    browser.open("https://go.gordon.edu/student/chapelcredits/viewattendance.cfm")

    soup = BeautifulSoup(browser.response().read())

    creditTable = soup.find_all('table')[8]

    creditRow = creditTable.find_all('tr')[0]
    creditCell = creditRow.find_all('td')[1]

    reqRow = creditTable.find_all('tr')[1]
    reqCell = reqRow.find_all('td')[1]

    return {
        "credit": int(creditCell.text),
        "required": int(reqCell.text)
    }

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

@app.route("/chapelcredit", methods=['GET'])
def main():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        chapelCredit = getChapelCredit(username, password, mechanize.Browser())
        return json.dumps(chapelCredit)
    else:
        return "Please only send GET requests. Bye!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(debug=True)
