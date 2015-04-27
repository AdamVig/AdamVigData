import requests, json, mechanize
from bs4 import BeautifulSoup

def get_student_id(username, password):
    """Get student id from Go Gordon"""

    # browser = mechanize.Browser()
    # browser.set_handle_robots(False)
    # browser.addheaders.append(('Authorization', 'Basic %s' % (username, password)))
    #
    # url = 'go.gordon.edu/lib/auth/level3logon.cfm?action=logon&password=122395IatW'
    # browser.open('https://' + username + ':' + password + '@' + url)
    # browser.select_form(name="form1")
    # browser['password'] = password
    # browser.submit()
    # print browser.response().read()
    # return

    print "reached"
    # url = 'go.gordon.edu/general/whoami.cfm'
    url = 'go.gordon.edu/lib/auth/level3logon.cfm?action=logon&password=122395IatW'
    response = requests.get('https://' + username + ':' + password + '@' + url)
    print response.text
    return

    if browser.response().code() == httplib.OK:
        page = BeautifulSoup(browser.response().read())

        student_id = page          \
            .find_all('table')[-1] \
            .find_all('tr')[-1]    \
            .find_all('td')[-1]    \
            .text

        return { 'data': student_id }

    else:
        return response.status_code

def serve_student_id(request, credentials):
    """Serve student id in JSON format"""

    student_id = get_student_id(credentials[0], credentials[1])
    return json.dumps(student_id)
