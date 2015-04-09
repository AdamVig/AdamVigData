def login_my_gordon(username, password, browser):
    """Login to My.Gordon.edu with given credentials
    Returns browser instance
    """

    browser.open("https://my.gordon.edu/ics")

    browser.select_form(name="MAINFORM")
    browser['userName'] = username
    browser['password'] = password
    browser.submit()

    return browser
