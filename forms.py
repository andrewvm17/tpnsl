from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    ##date_of_birth = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class MatchReportForm(FlaskForm):
    home_team = StringField('Home Team', validators=[DataRequired()])
    home_team_score = IntegerField('Home Team Score', validators=[DataRequired()])
    away_team = StringField('Away Team', validators=[DataRequired()])
    away_team_score = IntegerField('Away Team Score', validators=[DataRequired()])
    submit = SubmitField('Submit Report')
