"""Return a random error message."""
from config import ERROR_MESSAGE
import random


def get_mock_error(username, password):
    """Return a random error message."""
    error_message = random.choice(list(ERROR_MESSAGE.values()))

    return {
        'data': error_message
    }
