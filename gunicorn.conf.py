# gunicorn.conf.py
bind = '0.0.0.0:8000'
workers = 3
timeout = 120  # Set a higher timeout, for example, 120 seconds

