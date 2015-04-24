import base64

def get_credentials(request):
    """Retrieve username and password from request object
    Decode password using Base64 library
    """

    username = request.args.get('username')
    password = request.args.get('password')
    password = base64.b64decode(password)
    try:
        password = base64.b64decode(password)
    except:
        raise ValueError("Password is not properly Base64 encoded.")

    return username, password
