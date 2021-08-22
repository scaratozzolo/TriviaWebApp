from flask import Flask, session
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from app.users import User

app = Flask(__name__)
app.secret_key = 'scottstrivia'

app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()
sess.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////trivia.db'
db = SQLAlchemy(app)

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):

    if "join_game_data" in session:

        return User(session["join_game_data"]["user_name"], session["join_game_data"]["game_code"], session["join_game_data"]["user_id"])

    else:
        return None


from app import routes, socket_events, models

db.create_all()

