import os

os.system("/usr/local/bin/gunicorn --worker-class eventlet --bind 0.0.0.0:5000  -w 1 run:app")
