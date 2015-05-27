from config import *
import forecastio

def get_temperature(username, password):
    """Gets current temperature in Wenham, MA"""

    forecast = forecastio.load_forecast(FORECASTIO_API_KEY,
        WENHAM_LATITUDE,
        WENHAM_LONGITUDE)

    # Get temperature from forecast result
    temperature = forecast.currently().temperature

    # Round temperature to whole number
    temperature = int(temperature)

    return { 'data': temperature }
