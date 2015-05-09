import json, os, requests, base64, mechanize
from bs4 import BeautifulSoup
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin

import config, services
from chapelcredits import *
from checklogin import *
from daysleftinsemester import *
from mealpoints import *
from mealpointsperday import *
from nextmeal import *
from studentid import *

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "http://local.dev:8100",
    "supports_credentials": True }}, allow_headers='Content-Type')
app.config.from_object('config')
