from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')

class abcdForm(FlaskForm):
  abcd = RadioField('Make your choice:', choices=[('A','A'), ('B','B'),('C','C'),('D','D')], default='A')
  submit= SubmitField('Submit')