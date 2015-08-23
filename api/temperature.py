"""Get current temperature in Wenham, MA."""
from config import *
from services import db
from services import getdate
import forecastio


def get_temperature(username, password):
    """Get current temperature in Wenham, MA."""
    temperature = None
    cached_weather = db.get_doc('cache')['weather']

    time_expiration = getdate.parse_date_time(cached_weather['expiration'])
    time_now = getdate.get_date_time_object()

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
