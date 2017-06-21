from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from flaskext.mysql import MySQL
from dbqueryform import myDetails, myLocation


class AddUserForm(FlaskForm):
	name = StringField('Name of User:', validators=[DataRequired("Please enter the name of the newcomer.")])
	username= StringField('New Username:', validators=[DataRequired("Please enter a username.")])
	role = RadioField('Role of User:', choices=[('attendant','Room Attendant'),('supervisor','Supervisor')])
	password = PasswordField('New Password:', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Add User')

class CreateNewItem(FlaskForm):
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

class LoginForm(FlaskForm):
	username = StringField(validators=[DataRequired("Please enter a username")])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()


class RetrievalForm(FlaskForm):	
	amount = StringField('Input the amount taken', validators=[validators.input_required()])
	submit4 = SubmitField("Enter Quantity")


class AddNewLocation(FlaskForm):
	location = StringField('Location Tag', validators=[DataRequired("Please enter the location (no spaces)")])
	description= StringField('Description of Tag')
	submitThree = SubmitField("Enter")
	

class TrackingForm(FlaskForm):
	enabled = RadioField('Track item quantity? ', choices=[('yes','Yes'),('no','No')])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()