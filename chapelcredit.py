import json, os, requests
from bs4 import BeautifulSoup
from collections import OrderedDict
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

    # Successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text)

        creditTable = soup.find_all('table')[8]

        creditRow = creditTable.find_all('tr')[0]
        creditCell = creditRow.find_all('td')[1]

        reqRow = creditTable.find_all('tr')[1]
        reqCell = reqRow.find_all('td')[1]

        return {
            'credit': int(creditCell.text),
            'required': int(reqCell.text),
            'error': None
        }

    # Error
    else:
        return {
            'credit': 0,
            'required': 0,
            'error': response.status_code
        }

@app.route("/chapelcredit", methods=['GET'])
@cross_origin()
def main():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        chapelCredit = getChapelCredit(username, password)
        return json.dumps(chapelCredit)
    else:
        return "Wrong request type: " + request.method + ". Please only GET."

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
