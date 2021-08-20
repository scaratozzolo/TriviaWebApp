from flask import session
from flask_login import UserMixin
import string
import random



class User(UserMixin):


    def __init__(self, user_name, game_code, id=None):
        
        self.user_name = user_name
        self.game_code = game_code
        if id is None:
            self.id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=25))
        else:
            self.id = id

 
    def __eq__(self, other):

        return (self.user_name == other.user_name) and (self.game_code == other.game_code)

    def __repr__(self):
        return '<User: {}>'.format(self.user_name)