from app import socketio
from flask import request, session
from flask_socketio import join_room, leave_room, send, emit
from app.helpers import generate_game



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

    # print('received json: ' + str(json))
    # print(request.sid)
    send(json["user_name"] + ' has joined the game.', to=json["game_code"])


@socketio.on('hostGame')
def host_game(json):

    join_room(json["game_code"])


    send('host has joined the game.', to=json["game_code"])

    emit("gameQuestions", session.get('game_questions'), to=json["game_code"])



@socketio.on('startRound')
def start_round(json):

    # send(f'Round {json["round"]} starting...', to=json["game_code"])
    round_qs = session["game_questions"][f'{json["round"]}']

    round_cats = [round_qs[i]['category'] for i in round_qs]

    emit("startRoundPlayer", {'round': json['round'], 'cats': round_cats}, to=json["game_code"])


@socketio.on('startQuestion')
def start_question(json):

    gameround, question_num = json['question'].split("_")
    # send(f'Round {gameround}, Question {question_num} starting...', to=json["game_code"])
    
    q = session["game_questions"][gameround][json['question']]["question"]
    cat = session["game_questions"][gameround][json['question']]["category"]

    emit("startQuestionPlayer", {'question': q, 'category': cat, 'round': gameround, "question_num": question_num}, to=json["game_code"])


@socketio.on('endQuestion')
def end_question(json):

    gameround, question_num = json['question'].split("_")

    a = session["game_questions"][gameround][json['question']]["answer"]

    emit("endQuestionPlayer", {'answer': a, 'round': gameround, "question_num": question_num}, to=json["game_code"])

    session["scores"] = {k: v for k, v in sorted(session["scores"].items(), key=lambda item: item[1], reverse=True)}

    emit("scoreUpdate", session['scores'], to=json["game_code"])


@socketio.on('submitAnswerPlayer')
def submit_answer_player(json):

    gameround, question_num = json['question'].split("_")


    emit("submitAnswerHost", {'answer': json['answer'], 'points': json['points'], "user_name": json["user_name"], 'round': gameround, "question_num": question_num}, to=json["game_code"])


@socketio.on('markAnswer')
def submit_answer_player(json):

    gameround, question_num = json['question'].split("_")

    if json['user_name'] not in session['scores']:
        session['scores'][json['user_name']] = 0

    
    # TODO bonus questions - add a question type parameter
    # while generating questions, if last queston add a 'bonus' paramter to question data
    if json['status'] == 'correct':
        session['scores'][json['user_name']] += json['points']
    elif json['status'] == 'wrong':
        session['scores'][json['user_name']] -= json['points']

    