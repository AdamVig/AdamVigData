import json, os, requests, base64, mechanize
from bs4 import BeautifulSoup
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin

import chapelcredits, calculatemealpoints, mealpoints, studentid, services, \
daysleftinsemester, mealpointsperday

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
