from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired("Please enter your usename")])
	password = PasswordField('Password', validators=[DataRequired('Please enter a password')])
	submit = SubmitField("Sign in")


class RetrievalForm(Form):
	
	amount = StringField('Input the amount taken', validators=[validators.input_required()])
	submit = SubmitField("Enter Quantity")
