
from random import choices
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange



class CreateGameForm(FlaskForm):
    
    provider_select = RadioField("Question provider:", choices=[("open", "Open DB"), ("jep", "Jeopardy"), ("both", "Both")], default="both")
    num_rounds = IntegerField("# of rounds:", validators=[DataRequired(), NumberRange(1, 10)])
    num_questions = IntegerField("# of questions per round:", validators=[DataRequired(), NumberRange(1, 10)])
    submit = SubmitField('Submit')
    








class JoinGameForm(FlaskForm):

    game_code = StringField(validators=[DataRequired()])
    user_name = StringField(validators=[DataRequired()])
    submit = SubmitField('Join')

    def validate_game_code(self, game_code):
        # TODO check if game_code exists
        valid = False

        # temp to test
        if len(game_code.data) == 6:
            valid = True

        if not valid:
            raise ValidationError('Invlaid game code!')


    def validate_user_name(self, user_name):
        # TODO check game for name
        test = None
        if test is not None:
            raise ValidationError('Name already in use!')

