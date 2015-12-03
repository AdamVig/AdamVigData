"""Return a random error message."""
from config import ERROR_INFO
import random


def get_mock_error(username, password):
    """Raise a random error."""
    error_info = random.choice(list(ERROR_INFO.values()))

    raise ValueError(error_info)
