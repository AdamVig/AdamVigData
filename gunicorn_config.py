"""Configuration parameters for the gunicorn server."""
worker_class = "eventlet"
bind = '0.0.0.0:5000'
errorlog = '-'
