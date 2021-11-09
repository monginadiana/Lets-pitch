from wtforms import StringField,TextAreaField, SubmitField, SelectField
from wtforms.validators import Required, Length
from flask_wtf import FlaskForm

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class pitchForm(FlaskForm):
    pitcher = StringField("Submitted By: Your Name ...", validators = [Required()])
    title = StringField("Pitch Title", validators = [Required()])
    category = SelectField("What category are you submitting to?", choices=[("twitter", "Twitter"), ( "elevator", "Elevator"), ("competition", "Competition"), ("investor", "Investor")],validators=[Required()])
    description = TextAreaField('What pitch do you want to share?',validators = [Required()] )
    submit = SubmitField('Submit')
    

class CommentForm(FlaskForm):

    description = TextAreaField('Add a comment',validators = [Required()] )
    submit = SubmitField('Submit')

class Upvote(FlaskForm):
	submit = SubmitField()


class Downvote(FlaskForm):
	submit = SubmitField()