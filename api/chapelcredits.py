import requests, json
from bs4 import BeautifulSoup

def get_chapel_credits(username, password):
    """Get chapel credits from Go Gordon"""

    url = 'go.gordon.edu/student/chapelcredits/viewattendance.cfm'
    response = requests.get('https://' + username + ':' + password + '@' + url)

    if response.status_code == 200:

        if not "No Christian Life and Worship Credit Found" in response.text:
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
            return "No chapel credits found.", 404
    elif response.status_code == 401:
        return "Username and password do not match.", response.status_code
    else:
        return "Chapel credits are unavailable.", response.status_code
