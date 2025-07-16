from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, RadioField, HiddenField, DecimalField, IntegerField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')

class abcdForm(FlaskForm):
  abcd = RadioField('Make your choice:', choices=[('A','A'), ('B','B'),('C','C'),('D','D')], default='A')
  submit= SubmitField('Submit')
  
class tradingForm(FlaskForm):
    pounds = DecimalField()
    crypto = IntegerField()
    price = HiddenField()
    submit = SubmitField('Next Round')

class pythonMCQForm(FlaskForm):
    answer = HiddenField()
    abcd = RadioField('Answers:', choices=[('A','A'),('B','B'),('C','C'),('D','D')], default='A')
    submit = SubmitField('Submit')
    
class pythonDrillForm(FlaskForm):
    correct_answer = HiddenField()
    answer = StringField()
    submit = SubmitField('Submit')