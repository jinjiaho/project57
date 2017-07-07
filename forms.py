from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField, SelectField, BooleanField,DecimalField
from wtforms.validators import DataRequired, Email, Length
from flaskext.mysql import MySQL
from dbqueryform import myDetails, myLocation




class AddUserForm(FlaskForm):
	name = StringField('Name of User:', validators=[DataRequired("Please enter the name of the newcomer.")])
	username= StringField('New Username:', validators=[DataRequired("Please enter a username.")])
	role = RadioField('Role of User:', choices=[('runner','Runner'),('supervisor','Supervisor')])
	password = PasswordField('New Password:', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Add User')

class CreateNewItem(FlaskForm):

	itemname = StringField('Item Name', validators=[DataRequired("Please enter the name of the new item.")])
	category = SelectField('Category of Item', choices = myDetails('category'), validators = [DataRequired()])
	price = DecimalField('Unit Price', places=4, rounding=None, validators = [DataRequired()])
	# price = IntegerField('Unit Price',validators = [DataRequired()])
	reorderpt = IntegerField('Reorder point', validators = [DataRequired()])
	count_unit = StringField('Unit for counting', validators = [DataRequired()])
	order_unit = StringField('Unit for ordering', validators = [DataRequired()])
	order_multiplier = DecimalField('Qty in one unit ordered', places=4, rounding=None, validators = [DataRequired()])
	# order_multiplier = IntegerField('Qty in one unit ordered',validators = [DataRequired()])

	submitTwo = SubmitField('Add New Item')

class ExistingItemsLocation(FlaskForm):

	itemname = StringField('Item Name', validators=[DataRequired("Please insert the name of the item")])
	location = SelectField('Location of the Item', choices = myLocation('storeroom'), validators = [DataRequired()])
	tname = SelectField('Tag Name', choices=myLocation('tname'), validators=[DataRequired("Please select a tag")])
	qty = IntegerField('Available Amount', validators = [DataRequired()])
	submitFour = SubmitField('Add Location')

class LoginForm(FlaskForm):
	username = StringField(validators=[DataRequired("Please enter a username")])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()


class RetrievalForm(FlaskForm):
	amount = StringField('Input the amount taken', validators=[validators.input_required()])
	submit4 = SubmitField("Enter Quantity")


class AddNewLocation(FlaskForm):
	tname = StringField('Name of new tag', validators=[DataRequired("Please enter the name of the tag without spaces.")])
	location = StringField('Location of storeroom', validators=[DataRequired("Please enter the location.")])
	remarks = StringField('Remarks')
	submitThree = SubmitField("Enter")


class TrackingForm(FlaskForm):
	enabled = RadioField('Track item quantity? ', choices=[('yes','Yes'),('no','No')])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()
