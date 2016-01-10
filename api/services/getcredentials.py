"""Interpret user credentials."""
import base64


def get_credentials(args):
    """Interpret users credentials.

    Retrieves username and password from args object and decode password
    using Base64 library.
    """
    try:
        username = args.get('username')
        password = args.get('password')
    except:
        raise ValueError("Could not get credentials from args.")

    try:
        password = base64.b64decode(password)
    except:
        raise ValueError("Password is not properly Base64 encoded.")
    else:
        return username, password
