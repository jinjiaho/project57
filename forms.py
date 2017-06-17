from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class AddUserForm(FlaskForm):
	name = StringField('Name of User', validators=[DataRequired("Please enter the name of the newcomer.")])
	username= StringField('Create a Username', validators=[DataRequired("Please enter a username.")])
	role = RadioField('Role of User', choices=[('attendent','Room Attendant'),('supervisor','Supervisor')],validators=[DataRequired('Input Choice')])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Add User')

class LoginForm(FlaskForm):
	username = StringField(validators=[DataRequired("Please enter a username")])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()

class RetrievalForm(FlaskForm):	
	amount = StringField('Input the amount taken', validators=[validators.input_required()])
	submit = SubmitField("Enter Quantity")


