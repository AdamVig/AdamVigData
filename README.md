#AdamVigData
A personal API that currently serves as the backend for
[GoCo Student](https://github.com/adamvig/GoCoStudent).

## GoCo Student Endpoints
### About Endpoints
All GoCo Student endpoints begin with the prefix: `/gocostudent/[appversion]`.
For example, if the request is originating from version 2.2 of the app:
`/gocostudent/2.2/[endpoint]`.

Every GoCo Student endpoint accepts `GET` requests with username and password
parameters, like this:
`/gocostudent/[appversion]/[endpoint]?username=[username]&password=[password]`.
Obviously, fill in the brackets with data specific to your request. For example:
`/gocostudent/2.2/chapelcredits?username=adam.vigneaux&password=N0tMyP4ssw0rd`.

All endpoints return data in JSON format, usually with one key called `data`.
```
{
  "data": value
}
```

### About Status Codes
Each endpoint returns status codes and error messages relevant to the error that
it encountered. The error messages are concise enough to be displayed in the app.

+ Successful requests will receive a response of data accompanied with `200 OK`.
+ If a user gets past the `/checklogin` endpoint with an invalid login:
`401 UNAUTHORIZED`
+ If data is not found: `404 NOT FOUND`
+ If the server has an unidentified problem: `500 INTERNAL SERVER ERROR`
+ If something more specific goes wrong: [HTTP Status Codes Spec](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

### About Logging
Every request to the server is logged in the GoCo Student
[CouchDB](http://couchdb.apache.org/) database. This database is hosted for free
at [Cloudant](https://cloudant.com/). Each user's document in the database looks
like this:
```
{
  "_id": "[firstname.lastname]",    // Unique ID of document
  "_rev": "1-[random hash]",        // Unique revision number of document
  "dataCache": {                    // Actual data
    "mealPointsPerDay": 15,
    "mealPoints": 562,
    "chapelCredits": 29
  },
  "firstLogin": "2/18/15 12:57 AM", // Datetime of first request
  "dataRequests": {                 // Number of requests for each type of data
    "studentID": 62,
    "mealPointsPerDay": 127,
    "daysLeftInSemester": 168,
    "temperature": 26,
    "chapelCredits": 491,
    "studentInfo": 1,
    "nextMeal": 12,
    "mealPoints": 261
  },
  "lastLogin": "05/26/15 09:54 PM", // Datetime of latest request
  "totalLogins": 1961,              // Total number of requests
  "appVersion": "2.3",              // Latest version of app
  "privacyPolicy": "accepted"       // "accepted", "denied", or not set
}
```

### About Caching
Certain types of data are cached in the user's document in the database (noted
below in list of endpoints). Basically, only data that does not change often is
cached, with the notable exception of student ID because of the privacy policy.
The cache is intended to be used in the case of failure of Go Gordon or My Gordon
to respond to requests.

These types of data will only be cached if the user
has accepted the privacy policy, as denoted by `privacyPolicy: accepted`. If
the `privacyPolicy` key is not set in the user's data, the user should be
prompted with the privacy policy:

>Your password and student ID number are *never* stored anywhere except on your
>device.
> By default, data you access in this app is stored in a secure database to
>improve your user experience.
>Tap "Continue storing data" to agree to this privacy policy.

### List of Endpoints
Here is a list of endpoints you can retrieve data from:
+ `/chapelcredits`
  - includes "outof" key which indicates how many chapel credits are required
  - both data points are numbers
  - average response time: 2560ms
  - cached
  ```
  {
    "data": 29,
    "outof": 30
  }
  ```
+ `/chapelevents`
  - each event contains date, time, datetime, relative date, and event title
  - cached
  ```
  {
    "date": "Dec 9",
    "datetime": "Dec 9 10:25 AM",
    "relative": "in 12 days",
    "time": "10:25 AM",
    "title": "Chapel: Rev. Tom Haugen"
  },
  {...},
  ...
  ```
+ `/daysleftinsemester`
  - returns 0 if the semester is over
  - data is a number
  - average response time: 1150ms
  - *not* cached
  ```
  {
    "data": 72
  }
  ```
+ `/mealpoints`
  - decimal value is rounded up
  - data is a number
  - average response time: 5420ms
  - cached
  ```
  {
    "data": 562
  }
  ```
+ `/mealpointsperday`
  - return 0 if user has 0 mealpoints
  - decimal value is rounded up
  - data is a number
  - average response time: 5400ms
  - cached
  ```
  {
    "data": 15
  }
  ```
+ `/nextmeal`
  - gets menu for next meal from dining services page on Go Gordon
  - data is a string broken up by `\n` newline characters
  - *not* cached
  ```
  {
    "data": "Breakfast Menu\nIn Gillies: 9am-10:15am\nEggs to Order\n
    Egg Sandwiches to order\nPancakes to Order\nAssorted Pastry & Donuts\n
    Fruit\nCereal\nYogurt\nFruit\nJuice/Coffee/Tea"
  }
  ```
+ `/studentid`
  - splits student ID into two sections of four numbers for better display in app
  - data is a string
  - average response time: 2010ms
  - *not* cached
  ```
  {
    "data": "1234 5678"
  }
  ```
+ `/studentinfo`
  - gets full contents of whoami page on Go Gordon
  - value types:
    + `data` : `string`
    + `name` : `string`
    + `email` : `string`
    + `barcode` : `number` (14 digits long)
    + `id` : `number` (8 digits long)
  - average response time: untested
  - *not* cached
  ```
  {
    "data": "[name] [email] ID: [id] Barcode: [barcode]",
    "name": "[name]",
    "email": "email",
    "barcode": 12345678901234,
    "id": 12345678
  }
  ```
+ `/temperature`
  - only gets temperature for Wenham, no GPS support in app yet
  - data is a number
  - average response time: 1510ms
  - *not* cached
  ```
  {
    "data": 71
  }
  ```

There is one utility endpoint:
+ `/checklogin`
  - gets user data stored in GoCo Student database if login is valid and user
  exists
  - returns `401 UNAUTHORIZED` if login is invalid
  - average response time: 954ms

## How to Run This App
## 1. Clone this repository

```
cd [folder you want repository in]
git clone https://github.com/AdamVig/AdamVigData AdamVigData
```

## 2. Set up your [Virtualenv](https://virtualenv.pypa.io/en/latest/)

```
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

### If Virtualenv is not installed

```
pip install virtualenv
```

### If pip is not installed
Follow the installation instructions at [pip.pypa.io](https://pip.pypa.io/en/latest/installing.html#install-pip).

## 3. Set environment variables
You will need to set the following environment variables:

```
COUCH_SERVER = "[accountname].cloudant.com"
COUCH_DB_NAME = "gocostudent"
COUCH_USER = "[API key username]"
COUCH_PASS = "[API key secret]"
FORECASTIO_API_KEY = "[API key]"
```

In local development, you can set environment variables in a file called
`keys.py` (ignored by git). In production, they must be set as environment
variables. For example, using Heroku, you can set all the environment variables
in one command, with declarations separated by spaces:

```
heroku config:set COUCH_SERVER=[account name].cloudant.com COUCH_DB_NAME=gocostudent (etc...)
```

Sign up for a CloudAnt account (free CouchDB hosting)
[here](https://cloudant.com/sign-up/). Sign up for a ForecastIO account
(free weather API) [here](https://developer.forecast.io/register).

## 4. Run
### Local development:
This will run the app on `localhost:5000` and will reload automatically when the code
changes.

```
gunicorn -c gunicorn_config.py --reload run:app
```

### Production:
I recommend deploying the app via git to Heroku or some similar service. I use
Dokku, a Heroku clone running on a DigitalOcean VPS (Virtual Private Server).
Heroku and Dokku rely on the `Procfile` to describe how to run the app.

## 5. Testing
I test the app in local development using `curl`, for example:
`curl http://localhost:5000/gocostudent/2.3/chapelcredits?username=
[user]&password=[base64 encoded password]`

My unit tests are in `test.py`, which can be run to quickly make sure that
nothing is broken before deploying.
