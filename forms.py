from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, RadioField, HiddenField, DecimalField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')

class abcdForm(FlaskForm):
  abcd = RadioField('Make your choice:', choices=[('A','A'), ('B','B'),('C','C'),('D','D')], default='A')
  submit= SubmitField('Submit')
  
class pythonHelpForm(FlaskForm):
  code = HiddenField()
  submit = SubmitField('Get Help')
  
class tradingForm(FlaskForm):
    pounds = DecimalField()
    crypto = IntegerField()
    price = HiddenField()
    submit = SubmitField('Next Round')