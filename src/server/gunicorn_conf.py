import multiprocessing

bind = "0.0.0.0:8001"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog= '/var/log/gunicorn_access.log'
errorlog= '/var/log/gunicorn_error.log'
loglevel = "debug"
