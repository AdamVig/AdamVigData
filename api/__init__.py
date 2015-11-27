"""Import data getter modules."""
import json
import os
import requests
import base64

from bs4 import BeautifulSoup
from flask import Flask, request
from flask.ext.cors import CORS, cross_origin

import config
import services
from chapelcredits import *
from checklogin import *
from chapelevents import *
from daysleftinsemester import *
from mockerror import *
from mealpoints import *
from mealpointsperday import *
from nextmeal import *
from studentid import *
from studentinfo import *
from temperature import *

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "http://local.dev:8100",
    "supports_credentials": True}}, allow_headers='Content-Type')
app.config.from_object('config')
