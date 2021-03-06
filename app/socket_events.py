from app import socketio, db
from flask import request, session
from flask_socketio import join_room, leave_room, send, emit
from app.helpers import generate_game
from app.models import Game



# @socketio.on('disconnect')
# def disconnect():
#     print('Client disconnected')
#     print(request.sid)


# @socketio.on('connect')
# def connect():
#     print('Client connected')
#     print(request.sid)


@socketio.on('joinGame')
def join_game(json):

    join_room(json["game_code"])

    game = Game.query.filter_by(game_code=json["game_code"]).first()

    emit("playerJoinGame", {"num_players": len(game.users)}, to=json["game_code"])


@socketio.on('hostGame')
def host_game(json):

    join_room(json["game_code"])


    send('host has joined the game.', to=json["game_code"])

    emit("gameQuestions", session.get('game_questions'), to=json["game_code"])



@socketio.on('startRound')
def start_round(json):

    game = Game.query.filter_by(game_code=json["game_code"]).first()

    if json["round"] == 1:
        game.game_started = True
        

    game.cur_round = json["round"]
    db.session.commit()

    # send(f'Round {json["round"]} starting...', to=json["game_code"])
    round_qs = session["game_questions"][json["round"]]

    round_cats = [round_qs[i]['category'] for i in round_qs]

    emit("startRoundPlayer", {'round': json['round'], 'cats': round_cats}, to=json["game_code"])


@socketio.on('startQuestion')
def start_question(json):

    game = Game.query.filter_by(game_code=json["game_code"]).first()
    

    gameround, question_num = json['question'].split("_")
    # send(f'Round {gameround}, Question {question_num} starting...', to=json["game_code"])

    game.cur_question = int(question_num)
    game.cur_question_id = json['question']
    game.cur_question_started = True

    db.session.commit()

    question_data = session["game_questions"][int(gameround)][json['question']]
    
    q = question_data["question"]
    cat = question_data["category"]

    if question_data['bonus']:
        if int(gameround) == session["create_game_data"]["num_rounds"]:
            if int(gameround) != 1:
                max_points = ((10 * int(question_num)) // 2) * (int(gameround)//2) # (int(gameround) - 1)
            else:
                max_points = ((10 * int(question_num)) // 2)
        else:
            max_points = (10 * int(question_num)) // 2
    else:
        max_points = 10

    emit("startQuestionPlayer", {'question': q, 'category': cat, 'round': gameround, "question_num": question_num, "max_points": max_points}, to=json["game_code"])


@socketio.on('endQuestion')
def end_question(json):

    game = Game.query.filter_by(game_code=json["game_code"]).first()

    gameround, question_num = json['question'].split("_")

    game.cur_question_started = False
    db.session.commit()

    a = session["game_questions"][int(gameround)][json['question']]["answer"]

    emit("endQuestionPlayer", {'answer': a, 'round': gameround, "question_num": question_num}, to=json["game_code"])

    session["scores"] = {k: v for k, v in sorted(session["scores"].items(), key=lambda item: item[1], reverse=True)}

    emit("scoreUpdate", session['scores'], to=json["game_code"])


@socketio.on('submitAnswerPlayer')
def submit_answer_player(json):

    gameround, question_num = json['question'].split("_")


    emit("submitAnswerHost", {'answer': json['answer'], 'points': json['points'], "user_name": json["user_name"], 'round': gameround, "question_num": question_num}, to=json["game_code"])


@socketio.on('markAnswer')
def submit_answer_player(json):

    # if player doesn't answer, score stays same...should remove points?

    gameround, question_num = json['question'].split("_")

    if json['user_name'] not in session['scores']:
        session['scores'][json['user_name']] = 0


    if json['status'] == 'correct':
        session['scores'][json['user_name']] += json['points']
    elif json['status'] == 'wrong':
        session['scores'][json['user_name']] -= json['points']



@socketio.on('endGame')
def end_game(json):


    # TODO convert session scores to game.scores (probably do the same with questions too)
    emit("gameEnded", session['scores'], to=json["game_code"])

    leave_room(json["game_code"])


@socketio.on('leaveGame')
def leave_game(json):
    

    leave_room(json["game_code"])

    game = Game.query.filter_by(game_code=json["game_code"]).first()
    users = list(game.users)
    users.remove(json["user_name"])
    game.users = users
    db.session.commit()

    emit("playerLeftGame", {"num_players": len(game.users)}, to=json["game_code"])

    