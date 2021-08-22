from app import db
import bcrypt

class Game(db.Model):

    game_code = db.Column(db.String(6), primary_key=True)
    password = db.Column(db.String(256))


    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return password == self.password