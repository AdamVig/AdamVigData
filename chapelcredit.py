import json, os, requests, base64, mechanize
from bs4 import BeautifulSoup
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

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

    return app.make_response((json.dumps(chapelCredit), response.status_code))

@app.route("/chapelcredit", methods=['GET'])
@cross_origin(origins='http://local.dev:8100', supports_credentials=True)
def main():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        password = base64.b64decode(password)
        return getChapelCredit(username, password)
    else:
        return app.make_response(("Please only use GET requests.", 401))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
