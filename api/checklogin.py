"""Verify that login is valid using Gordon's servers."""
import httplib
import requests
from services import db
from config import ERROR_INFO


def check_login(username, password):
    """Validate login on Go Gordon."""
    url = 'https://go.gordon.edu/'

    try:
        response = requests.head(url, auth=(username, password))

    except requests.exceptions.RequestException:
        raise ValueError(ERROR_INFO['INTERNAL_SERVER_ERROR'])

    else:
        if response.status_code == httplib.OK:
            #try:
                #user = db.get_doc(username)
            #except ValueError:
                #print "Valid login but user does not exist in database."
            #else:
                #return {'data': user}

            return {'data': {}}

        elif response.status_code == httplib.UNAUTHORIZED:
            raise ValueError(ERROR_INFO['UNAUTHORIZED'])

        else:
            raise ValueError(ERROR_INFO['INTERNAL_SERVER_ERROR'])
