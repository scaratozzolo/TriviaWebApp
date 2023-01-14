from importlib import import_module
from flask import Flask, session
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from app.users import User



sess = Session()

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):

    if "join_game_data" in session:

        return User(session["join_game_data"]["user_name"], session["join_game_data"]["game_code"], session["join_game_data"]["user_id"])

    else:
        return None


def register_extensions(app):
    sess.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)


def register_blueprints(app):
    # for module_name in ("auth", "index"):
    #     module = import_module('app.{}.routes'.format(module_name))
    #     app.register_blueprint(module.blueprint)

    module = import_module('app.routes')
    app.register_blueprint(module.all_blueprint)

    module = import_module('app.socket_events')


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    # @app.errorhandler(403)
    # def access_forbidden(error):
    #     return render_template('index/page-403.html'), 403


    # @app.errorhandler(404)
    # def not_found_error(error):
    #     return render_template('index/page-404.html'), 404


    # @app.errorhandler(500)
    # def internal_error(error):
    #     return render_template('index/page-500.html'), 500
    return app