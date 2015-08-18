"""Get current temperature in Wenham, MA."""
from config import *
from services import db
from services import getdate
import forecastio
from datetime import timedelta


def get_temperature(username, password):
    """Get current temperature in Wenham, MA."""
    cached_weather = db.get_app_info()['weather']

    updated_time = getdate.parse_date_time(cached_weather['updated'])
    time_now = getdate.get_date_time_object()
    time_since_updated = time_now - updated_time

    update_interval = timedelta(0, 0, 0, 0, WEATHER_UPDATE_INTERVAL_MINUTES)

    if time_since_updated < update_interval:
        return {'data': cached_weather['temperature']}
    else:
        forecast = forecastio.load_forecast(FORECASTIO_API_KEY,
                                            WENHAM_LATITUDE,
                                            WENHAM_LONGITUDE)

        # Get temperature from forecast result
        temperature = forecast.currently().temperature

        # Round temperature to whole number
        temperature = int(temperature)

        weather = {
            'temperature': temperature,
            'updated': getdate.get_date()
        }

        db.save_app_info("weather", weather)

    return {'data': temperature}
