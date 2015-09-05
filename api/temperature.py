"""Get current temperature in Wenham, MA."""
from config import *
import arrow
from services import db
import forecastio


def get_temperature(username, password):
    """Get current temperature in Wenham, MA."""
    temperature = None
    cached_weather = db.get_doc('cache')['weather']

    try:
        time_expiration = arrow.get(
            cached_weather['expiration'],
            DATETIME_FORMAT)
    except arrow.parser.ParserError:
        time_expiration = None

    time_now = arrow.now(TIMEZONE)

    if time_now < time_expiration:
        temperature = cached_weather['temperature']
    else:
        forecast = forecastio.load_forecast(FORECASTIO_API_KEY,
                                            WENHAM_LATITUDE,
                                            WENHAM_LONGITUDE)

        # Get temperature from forecast result
        temperature = forecast.currently().temperature

        # Round temperature to whole number
        temperature = int(temperature)

        weather_data = {
            'temperature': temperature
        }

        db.cache_app_data('weather',
                          weather_data,
                          WEATHER_UPDATE_INTERVAL_MINUTES)

    return {'data': temperature}
