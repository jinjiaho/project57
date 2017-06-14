from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
import os
import copy
from forms import LoginForm, RetrievalForm
import csv
# from flask.ext.cache import Cache

app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = "development-key"

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'classroom'
app.config['MYSQL_DATABASE_DB'] = 'Ascott_InvMgmt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
adminmode = False

role = ""

#----------------------------METHODS-------------------------
# Returns all the items based on category and amount in or out within the last month for each item
def getAllInventory(category):
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute(
		"SELECT sku, name, qty_left, unit, picture FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))
	data = cursor.fetchall()
	items = []
	for item in data:
		cursor.execute(
			"SELECT action, qty_moved FROM ascott_invmgmt.logs WHERE month(date_time) = month(now()) AND year(date_time) = year(now()) AND item='{}';".format(item[0]))
		in_out_data = cursor.fetchall()
		delivered_out = 0
		recieved = 0
		for i in in_out_data:
			if i[0].encode('ascii') == 'out':
				delivered_out = delivered_out + (-1*int(i[1]))
			elif i[0].encode('ascii') == "in":
				recieved = recieved + int(i[1])
		remaining_quantity = item[2]
		initial_quantity = remaining_quantity + delivered_out - recieved
		items.append(
			{"name": item[1],
			"remaining": item[2],
			"unit": item[3],
			"starting": initial_quantity,
			"recieved": recieved,
			"demand": delivered_out,
			"file": item[4]})
		
	return items


# Returns all the items based on location. KIV for possible supervisor view filtering.
def getFromLevels(location):
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT name, category, location FROM Ascott_InvMgmt.Items WHERE location = '{}';".format(location))

	data=cursor.fetchall()
	things = []
	for item in data:
		things.append(
			{"name": item[0],
			"category": item[1],
			"location":item[2]})
	return things



# Returns the logs that occurred within the current month.
def getAllLogs():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(
		"SELECT user, date_time, action, qty_moved, qty_left, item, location FROM Ascott_InvMgmt.Logs WHERE month(date_time) = month(now()) AND year(date_time) = year(now());")
	data=cursor.fetchall()
	things = []
	
	for row in data:

		# cursor.execute("SELECT name, category FROM Ascott_InvMgmt.Items WHERE name = {};".format(str(row[5])))
		# item_data=cursor.fetchone()

		things.append({"name": row[0].encode('ascii'),
			"dateTime": row[1],
			"action":row[2],
			"move":row[3],
			"remaining":row[4],
			"item":row[5].encode('ascii'),
			"location":row[6]})
		print(things)

			

	return things
		

# TEST: extract dummy inventory qty data for Highcharts
def extract():
	with open("inventory.csv", 'rU') as f:  #opens file
	    reader = csv.reader(f)
	    data = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists
	return data

# POST for getting chart data
@app.route('/api/getData', methods=["POST"])
def getData():

	print "content_type: ", request.content_type
	print "request.json: ", request.json

	data = str(request.get_json())
	# print(data, type(data))

	if not request.json:
	    print "Bad json format"
	    abort(400)
	else:
		conn = mysql.connect()
		cursor = conn.cursor()

		# TODO: string parameterisation
		query = "SELECT sku FROM Ascott_Invmgmt.Items WHERE name = '{}';".format(request.json)

		cursor.execute(query)
		idItem = cursor.fetchone()[0]
		# print(idItem)

		# query = "SELECT date_time, qty_left FROM Ascott_Invmgmt.Logs WHERE item = {0}".format(idItem)
		query = "SELECT date_time, qty_left FROM Ascott_Invmgmt.Logs WHERE item = 1"
		# TODO: string parameterisation
		# query = "SELECT datetime, qtyAfter FROM Ascott_Invmgmt.Logs WHERE idItem = {}".format(idItem)
		cursor.execute(query)
		responseData = cursor.fetchall()

		return jsonify(responseData)


# true if user is authenticated, else false
def auth():
	# print session.keys()[0], type(session.keys()[0])
	if u'logged_in' in session:
		# print session['logged_in'], type(session['logged_in'])
		return session['logged_in']
	# else:
		# print "You're not logged in"
	return False

#----------------------------ROUTING ------------------------

@app.route('/')
def hello():
	if session.get('logged_in'):
		if role == 'supervisor':
			return redirect('/dashboard')
		else:
			return redirect('/dashboard')
	else:
		return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
	
	error = ""
	# create a login form to collect username & password
	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else: 
			username = form.username.data
			password = form.password.data
		
			cursor=mysql.connect().cursor()
			cursor.execute("SELECT username, password, role FROM User WHERE username= '" + username + "';")

			# check if user and pass data is correct by executing the db
			# data is stored as a tuple
			data = cursor.fetchone()
	
			if data is None: 
				# username does not match records
				flash('User does not exist')
				return redirect('/login')

			elif password != data[1]:
				# password does not match records
				flash('Incorrect password')
				return redirect('/login')

			else:
				# username & password match
				session['username'] = data[0]
				session['role'] = data[2]
				session['logged_in'] = True

				# check role
				if data[2] == "supervisor":
					return redirect('/dashboard')
				elif data[2] =="attendant":
					return redirect('/scan')

	elif request.method =="GET":

		# user authentication
		logged_in = auth()
		if not logged_in:
			return render_template('login.html', form=form)

		# user already logged in previously
		if session['role'] == "supervisor":
			return redirect('/dashboard')
		elif session['role'] =="attendant":
			return redirect('/scan')


@app.route('/dashboard')
def dashboard():

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect('/login')

	return render_template('dashboard.html', user=session['username'])


@app.route('/inventory/')
def inventory():
	# conn = mysql.connect()
	# cursor = conn.cursor()

	# cursor.execute(
	# 	"SELECT sku, name, qty_left, unit, picture, category FROM Ascott_InvMgmt.Items;")
	# data = cursor.fetchall()
	# items = {}
	# for i in data:
	# 	if i[5] not in items:
	# 		items[i[5]] = []
	# 		print("new category created: "+str(i[5]))
	# 	items[i[5]].append({'name':i[1],
	# 		'remaining':i[2],
	# 		'unit':i[3],
	# 		'picture':i[4]})

	# print(items)

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect('/login')
			
	# get current list of all items listed in db
	supplies = getAllInventory('Guest Supplies')
	hampers = getAllInventory('Guest Hampers')
	kitchenware = getAllInventory('Kitchenware')
	return render_template('inventory.html',
		supplies = supplies,
		hampers = hampers,
		kitchenware = kitchenware)

@app.route('/inventory/<item>')
def item(item):

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect('/login')

	name = item
	conn = mysql.connect()
	cursor = conn.cursor()

	query = "SELECT sku, name, picture, category FROM Ascott_Invmgmt.Items WHERE name = '{0}';".format(name)

	cursor.execute(query)
	data = cursor.fetchall()
	try:
		sku = data[0][0]
		picture = data[0][2]
		category = data[0][3]
		return render_template('item.html', 
			item=item, 
			sku = sku,
			picture = picture,
			category = category,
			user = session['username'])
	except:
		return render_template('item.html', item=item, sku=None, picture=None, category=None, user=session['username'])

# @app.route('/inventory/<category>')
# def category(category):
# 	category = category
# 	itemtype = getAllInventory(category)
# 	return render_template('category.html', category=category, itemtype=itemtype, 
# 		role = role,
# 		user = session['username'])


@app.route('/logs')
def logs():

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect('/login')

	logs=getAllLogs()
	# names=getUniqueNames()
	# items=getUniqueItems()
	return render_template('logs.html',
		logs=logs, 
		role = role,
		user = session['username'])
	# names=names, items=items)

@app.route('/scan')
def scanner():
	return render_template('scanner.html')

# RA shelf view
@app.route('/shelves/<tag_id>/', methods=['GET', 'POST'])
# @cache.cached(timeout=50)
def shelf(tag_id):

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect('/login')

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT sku, name, category, picture FROM Ascott_InvMgmt.Items WHERE location = '{}';".format(tag_id))

	data=cursor.fetchall()
	things = []
	for item in data:
		things.append(
			{"sku":item[0],
			"name": item[1],
			"category": item[2],
			"picture":item[3]})
	return render_template('storeroom.html', things=things, 
		role = role,
		user = session['username'], 
		location = tag_id)


# @app.route('/shelves/<tag_id>/cart', methods=['GET', 'POST'])
# def checkout(tag_id):
# 	if request.method == 'GET':
# 		return render_template('cart.html')
# 	else:
# 		now = datetime.now()
# 		form_data = request.form
# 		user = session['username']
		
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		for item, qty in form_data.iteritems():
# 			cursor.execute("INSERT INTO Logs (user, date_time, action, qty_moved, name, location) VALUES ({}, {}, 'retrieval', {}, {}, {});".format(user, now, qty, item, tag_id))

# 		flash("Success!")
# 		return redirect('scanner.html')

# @app.route('/storeroom/')
# def storeroom():
# #get data input from location from mobilephone. data output from db is in tuple
# #this userinput is hard coded
# 	catItems = getFromLevels("Level4C2")
# 	return render_template("storeroom.html", catGoods=catItems)

# @app.route('/storeroom/<things>', methods=["GET","POST"])	
# def retrieval(things):
# 	things=things
# 	form = RetrievalForm()


# 	if request.method == "POST":
# 		if form.validate() == False:
# 			return render_template("retrieval.html",things=things,form=form)
# 		elif type(form.amount.data)!=int:
# 			return render_template("retrieval.html",things=things,form=form)

# 		else:	
# 			input = form.amount.data
			
# 			# flash('this has been added to the cart')
# 			# return redirect(url_for('storeroom/'))
# 			return ('you did it!!!!!')


# 	elif request.method=="GET":
# 		return render_template('retrieval.html',things=things, form=form)

# 	return render_template("retrieval.html", things=things)

@app.route('/logout')
def logout():
	session.clear();
	role = None
	return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, nothing at this URL.', 404


## testing
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')