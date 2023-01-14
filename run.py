from app import create_app, socketio
from app.config import Config

app = create_app(Config)


if __name__ == '__main__':

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    # gunicorn --worker-class eventlet --bind 0.0.0.0:5000  -w 1 run:app
    # app.run(host="0.0.0.0", port=5000, debug=True)