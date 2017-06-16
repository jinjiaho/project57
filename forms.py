from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField
from wtforms.validators import DataRequired, Email, Length

class AddUserForm(Form):
	name = StringField('Name of User:', validators=[DataRequired("Please enter the name of the newcomer.")])
	username= StringField('New Username:', validators=[DataRequired("Please enter a username.")])
	role = RadioField('Role of User:', choices=[('attendent','Room Attendant'),('supervisor','Supervisor')],validators=[DataRequired('Input Choice')])
	password = PasswordField('New Password:', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Add User')

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired("Please enter your usename")])
	password = PasswordField('Password', validators=[DataRequired('Please enter a password')])
	submit = SubmitField("Sign in")

class RetrievalForm(Form):	
	amount = StringField('Input the amount taken', validators=[validators.input_required()])
	submit = SubmitField("Enter Quantity")


