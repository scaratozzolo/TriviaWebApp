from app import db

class Game(db.Model):
    # TODO add game message?
    game_code = db.Column(db.String(6), primary_key=True)
    password = db.Column(db.String(256))
    num_rounds = db.Column(db.Integer)
    num_questions = db.Column(db.Integer)
    provider = db.Column(db.String(10))
    game_started = db.Column(db.Boolean)
    game_msg = db.Column(db.String(512))


    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return password == self.password