from app import db

class Game(db.Model):
    # TODO scores, game questions, max players
    game_code = db.Column(db.String(6), primary_key=True)
    password = db.Column(db.String(256))
    num_rounds = db.Column(db.Integer)
    num_questions = db.Column(db.Integer)
    provider = db.Column(db.String(10))
    game_msg = db.Column(db.String(512))

    users = db.Column(db.PickleType)

    game_started = db.Column(db.Boolean)
    cur_round = db.Column(db.Integer)
    cur_question = db.Column(db.Integer)
    cur_question_id = db.Column(db.String(6))
    cur_question_started = db.Column(db.Boolean)


    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return password == self.password