from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import JoinGameForm, CreateGameForm
from app.users import User
from app.helpers import generate_game, generate_round
from app import app, socketio
import string
import random

@app.route('/', methods=['GET', 'POST'])
def index():

    # if "join_game_data" in session:
    if current_user.is_authenticated:
        return redirect(f"/game/{session['join_game_data']['game_code']}")


    form = JoinGameForm()

    if form.validate_on_submit():
        form.game_code.data = form.game_code.data.upper()
        session["join_game_data"] = form.data

        user = User(form.user_name.data, form.game_code.data)
        login_user(user)

        session["join_game_data"]['user_id'] = user.get_id()

        return redirect(f"/game/{form.game_code.data}")

    return render_template('index.html', title='Home', form=form)



@app.route('/create', methods=['GET', 'POST'])
def create_game():


    form = CreateGameForm()
    if form.validate_on_submit():

        # todo create game, get all questions and store somehow
        session["create_game_data"] = form.data
        
        game_code = ''.join(random.choices(string.ascii_uppercase, k=6))
        session["create_game_data"]["game_code"] = game_code

        # for round in range(1, session["create_game_data"]["num_rounds"]+1):
        #     questions = generate_round(round, session["create_game_data"]["num_rounds"], session["create_game_data"]["num_questions"], session["create_game_data"]["provider_select"])
        #     session[f"game_questions_{round}"] = questions

        questions = generate_game(session["create_game_data"]["num_rounds"], session["create_game_data"]["num_questions"], session["create_game_data"]["provider_select"])
        session[f"game_questions"] = questions

        session["scores"] = {}


        return redirect(f"/game/{game_code}/host")
        # return session["create_game_data"]

    return render_template('create.html', title='Create Game', form=form)



@app.route('/game/<game_code>/host')
def host_game(game_code):

    if "create_game_data" not in session:
        return redirect("/")

    return render_template("host_dash.html", title="Host Dashboard")




@app.route('/game/<game_code>')
@login_required
def play_game(game_code):

    if "join_game_data" not in session:
        return redirect("/")

    return render_template("play_game.html", title="Play Trivia")



# for testing purposes
@app.route("/clearsession")
def clearsession():
    
    session.pop("join_game_data", None)
    session.pop("create_game_data", None)
    session.pop("game_questions", None)
    print("session data cleared")

    return redirect("/")
