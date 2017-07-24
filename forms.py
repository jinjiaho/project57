from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators, IntegerField, SelectField, BooleanField,DecimalField
from wtforms.validators import DataRequired, Email, Length
from flaskext.mysql import MySQL

class AddUserForm(FlaskForm):
	name = StringField('Full Name', validators=[DataRequired("Please enter the name of the newcomer.")])
	username= StringField('Username', validators=[DataRequired("Please enter a username.")])
	role = RadioField('Role of User')
	password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
	submit = SubmitField('Add User')

class CreateNewItem(FlaskForm):

	itemname = StringField('Item Name', validators=[DataRequired("Please enter the name of the new item.")])
	category = SelectField('Category of Item', validators = [DataRequired()])
	price = DecimalField('Unit Price', places=4, rounding=None, validators = [DataRequired()])
	reorderpt = IntegerField('Reorder Point', validators = [DataRequired()])
	count_unit = SelectField('Unit for Withdrawal', validators = [DataRequired()], choices=[("carton", "carton"), ("pc", "pc"), ("kg", "kg"), ("tin", "tin"), ("box", "box"), ("unit", "unit"), ("packet", "packet")])
	order_unit = SelectField('Unit for Purchasing', validators = [DataRequired()], choices=[("carton", "carton"), ("pc", "pc"), ("kg", "kg"), ("tin", "tin"), ("box", "box"), ("unit", "unit")])
	order_multiplier = DecimalField('Item Qty per Unit Ordered', places=4, rounding=None, validators = [DataRequired()])
	submitTwo = SubmitField('Add New Item')

class ExistingItemsLocation(FlaskForm):

	itemname = StringField('Item Name', validators=[DataRequired("Please insert the name of the item")])
	tid = SelectField('Tag', coerce=int) # Value is tid
	qty = IntegerField('Available Amount', validators = [DataRequired()])
	submitFour = SubmitField('Assign To Tag')

class TransferItem(FlaskForm):
	iname = StringField('Item Name')
	tagOld = SelectField('Old Tag', coerce=int) # Value is tid
	tagNew = SelectField('New Tag', coerce=int) # Value is tid
	qty = IntegerField('Qty to Transfer', [validators.Optional()])
	submit = SubmitField()

class LoginForm(FlaskForm):
	username = StringField(validators=[DataRequired("Please enter a username")])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()


class RetrievalForm(FlaskForm):
	amount = StringField('Input the Amount Taken', validators=[validators.input_required()])
	submit4 = SubmitField("Enter Quantity")


class AddNewLocation(FlaskForm):
	tname = StringField('Name of New Tag', validators=[DataRequired("Please enter the name of the tag without spaces.")])
	location = SelectField('Select Storeroom', validators = [DataRequired()])
	newLocation = StringField('Add a New Storeroom')
	remarks = StringField('Remarks (optional)')
	submitThree = SubmitField("Enter")


class TrackingForm(FlaskForm):
	enabled = RadioField('Track Item Quantity? ', choices=[('yes','Yes'),('no','No')])
	password = PasswordField(validators=[DataRequired('Please enter a password')])
	remember = BooleanField()
	submit = SubmitField()

class RemoveItem(FlaskForm):
	iname = StringField('Item Name')
	submit = SubmitField("Delete Item")

class RemoveTag(FlaskForm):
	tid = SelectField('Tag', coerce=int)
	submit = SubmitField()


