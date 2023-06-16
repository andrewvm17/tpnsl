from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    ##date_of_birth = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class MatchReportForm(FlaskForm):
    division = SelectField('Division', choices=[('coed10', 'CoEd 10')])
    home_team = SelectField('Home Team', choices=[('lime_green', 'Lime Green'), ('black', 'Black'), ('purple', 'Purple'),('forest_green', 'Forest Green'), ('red', 'Red'), ('gold', 'Gold')], validators=[DataRequired()])
    home_team_score = IntegerField('Home Team Score', validators=[DataRequired()])
    away_team = SelectField('Away Team', choices=[('lime_green', 'Lime Green'), ('black', 'Black'), ('purple', 'Purple'),('forest_green', 'Forest Green'), ('red', 'Red'), ('gold', 'Gold')], validators=[DataRequired()])
    away_team_score = IntegerField('Away Team Score', validators=[DataRequired()])
    date = DateField('Match Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Report')
