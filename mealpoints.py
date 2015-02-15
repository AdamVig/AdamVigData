import mechanize, json
from bs4 import BeautifulSoup
from collections import OrderedDict
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

# Login to My.Gordon.edu with given credentials
# Returns browser instance
def loginMyGordon(username, password, browser):
    browser.open("https://my.gordon.edu/ics")
    browser.select_form(name="MAINFORM")
    browser['userName'] = username
    browser['password'] = password
    browser.submit()
    return browser

# Get meal points from My.Gordon.edu for given user
# Returns number of meal points
def getMealPoints(username, password, browser):
    browser = loginMyGordon(username, password, browser)

    studentsLink = browser.find_link(url="./Students/")
    browser.follow_link(studentsLink)

    mealpointsLink = browser.find_link(url="/ICS/Students/Mealpoints.jnz")
    browser.follow_link(mealpointsLink)
    headers = [
        ('Cookie', "ASP.NET_SessionId=55zcxgufse0frq3jyzpkxj5r; _ga=GA1.2.151033858.1421028027; __utmt=1; __utma=156794413.151033858.1421028027.1422829862.1422836737.8; __utmb=156794413.10.10.1422836737; __utmc=156794413; __utmz=156794413.1421261850.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); .sessionheartbeat=2/1/2015 8:36:31 PM"),
        ('Referer', "https://my.gordon.edu/gmex/home/bounce?fwkid=deff9811-eb12-4572-8302-da42ebcf29d1")
    ]
    browser.addheaders = headers;
    browser.open("https://my.gordon.edu/GMEX")
    print browser.geturl()
    soup = BeautifulSoup(browser.response().read())
    print soup
