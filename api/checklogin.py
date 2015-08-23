"""Verify that login is valid using Gordon's servers."""
import httplib
import requests
from services import db
from config import error_message


def check_login(username, password):
    """Validate login on Go Gordon."""
    url = 'https://go.gordon.edu/'

    try:
        response = requests.head(url, auth=(username, password))

    except requests.exceptions.RequestException:
        raise ValueError(error_message['INTERNAL_SERVER_ERROR'],
                         httplib.INTERNAL_SERVER_ERROR)

    else:
        if response.status_code == httplib.OK:
            try:
                user = db.get_doc(username)
            except ValueError:
                print "Valid login but user does not exist in database."
            else:
                return {'data': user}

        elif response.status_code == httplib.UNAUTHORIZED:
            raise ValueError(error_message['UNAUTHORIZED'],
                             httplib.UNAUTHORIZED)

        else:
            raise ValueError(error_message['INTERNAL_SERVER_ERROR'],
                             httplib.INTERNAL_SERVER_ERROR)
