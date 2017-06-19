from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flaskext.mysql import MySQL
from dbqueryform import myDetails, myLocation



class AddUserForm(Form):
	name = StringField('Name of User:', validators=[DataRequired("Please enter the name of the newcomer.")])
	username= StringField('New Username:', validators=[DataRequired("Please enter a username.")])
	role = RadioField('Role of User:', choices=[('attendent','Room Attendant'),('supervisor','Supervisor')])
	password = PasswordField('New Password:', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Add User')

class CreateNewItem(Form):
	sku = StringField('SKU Number', validators = [DataRequired()])
	itemname = StringField('Item Name', validators=[DataRequired("Please enter the name of the newcomer.")])
	location = SelectField('Location of the Item', choices = myLocation('location'), validators = [DataRequired()]) 
	qtyleft = IntegerField('Available Amount', validators = [DataRequired()])
	reorderpt = IntegerField('Reorder point', validators = [DataRequired()])
	batchqty = IntegerField('Batch size: ', validators = [DataRequired()])
	category = SelectField('Category of Item', choices = myDetails('category'), validators = [DataRequired()]) 
	picture = StringField('Full Name for the file', validators = [DataRequired()])
	unit = SelectField('Unit Size', choices = myDetails('unit'), validators = [DataRequired()]) 
	submitTwo = SubmitField('Add New Item')

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired("Please enter your usename")])
	password = PasswordField('Password', validators=[DataRequired('Please enter a password')])
	submit = SubmitField("Sign in")


class RetrievalForm(Form):	
	amount = StringField('Input the amount taken', validators=[validators.input_required()])
	submit4 = SubmitField("Enter Quantity")


class AddNewLocation(Form):
	location = StringField('Location Tag', validators=[DataRequired("Please enter the location (no spaces)")])
	description= StringField('Description of Tag')
	submitThree = SubmitField("Enter")
	

