import requests, json
from bs4 import BeautifulSoup

def get_chapel_credits(username, password):
    """Get chapel credits from Go Gordon"""

    url = 'go.gordon.edu/student/chapelcredits/viewattendance.cfm'
    response = requests.get('https://' + username + ':' + password + '@' + url)

    if response.status_code == 200:
        page = BeautifulSoup(response.text)

        credit_table = page.find_all('table')[8]

        credits = credit_table \
            .find_all('tr')[0] \
            .find_all('td')[1] \
            .text

        required = credit_table \
            .find_all('tr')[1]  \
            .find_all('td')[1]  \
            .text

        return {
            'data': int(credits),
            'outof': int(required)
        }, 200

    else:
        return "Chapel credits are unavailable", response.status_code
