import mechanize, json
from bs4 import BeautifulSoup
from collections import OrderedDict
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)


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

@app.route("/chapelcredit", methods=['GET', 'POST'])
@cross_origin()
def main():
    if request.method == 'POST':
        username = request.args.get('username')
        password = request.args.get('password')
        chapelCredit = getChapelCredit(username, password, mechanize.Browser())
        return json.dumps(chapelCredit)
    else:
        return "Please only send GET requests. Bye!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
