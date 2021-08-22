
from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from app.models import Game



class CreateGameForm(FlaskForm):
    
    provider_select = RadioField("Question provider:", choices=[("open", "Open DB"), ("jep", "Jeopardy"), ("both", "Both")], default="both")
    num_rounds = IntegerField("# of rounds:", validators=[DataRequired(), NumberRange(1, 10)])
    num_questions = IntegerField("# of questions per round:", validators=[DataRequired(), NumberRange(1, 10)])
    password = PasswordField("Password (optional):")
    game_msg = StringField("Message to players:")
    submit = SubmitField('Submit')

    def validate_game_msg(self, game_msg):

        if len(game_msg.data) > 512:
            raise ValidationError(f'Game message must be less than 512 characters! Currently {len(game_msg.data)}.')

    



class JoinGameForm(FlaskForm):

    game_code = StringField("Game Code", validators=[DataRequired()])
    password = PasswordField("Password (if required)")
    user_name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField('Join')

    def validate_game_code(self, game_code):

        game = Game.query.filter_by(game_code=game_code.data).first()

        if game is None:
            raise ValidationError('Invalid game code!')

    
    def get_game_code(self):
        return self.game_code

    def validate_password(self, password):

        game = Game.query.filter_by(game_code=self.get_game_code().data).first()

        if not game:
            return None

        if not game.check_password(password.data):
            raise ValidationError('Password incorrect')


    def validate_user_name(self, user_name):
        # TODO check game for name
        test = None
        if test is not None:
            raise ValidationError('Name already in use!')

