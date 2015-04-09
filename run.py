from api import *


endPoint = '/gocostudent/<version>/'

@app.route(endPoint + 'chapelcredits', methods=['GET', 'HEAD'])
def route_chapel_credits(version):
    credentials = services.getcredentials.get_credentials(request)
    if request.method == 'GET':
        data = chapelcredits.get_chapel_credits(credentials[0], credentials[1])
        return app.make_response((json.dumps(data[0]), data[1]))
    else:
        return app.make_response(("Chapel credits endpoint is working.", 200))

@app.route(endPoint + 'mealpoints', methods=['GET', 'HEAD'])
def route_meal_points():
    credentials = services.getcredentials.get_credentials(request)
    if request.method == 'GET':
        data = mealpoints.get_meal_points(credentials[0], credentials[1])
        return app.make_response((json.dumps(data[0]), data[1]))
    else:
        return app.make_response(("Meal points endpoint is working.", 200))

@app.route('/', methods=['GET'])
def route_default():
    return "The app server is running correctly."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
