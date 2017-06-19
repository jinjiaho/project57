from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, g
from flask_babel import Babel
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from forms import LoginForm, RetrievalForm, AddUserForm
import os, copy, re, csv
# from flask.ext.cache import Cache


##########################
##        CONFIG        ##
##########################
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DevConfig') # default configurations
app.config.from_pyfile('myConfig1.cfg') # override with instanced configuration (in "/instance"), if any

# Babel init
babel = Babel(app)
languages = ('en', 'zh', 'ms', 'ta')

# mysql init
mysql = MySQL()
mysql.init_app(app)

# global vars
adminmode = False
role = ""

###########################
##        METHODS        ##
###########################

# TODO: encapsulate all methods in separate classes and .py files

# Returns all the items based on category and amount in or out within the last month for each item
def getAllInventory(category):
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute(
		"SELECT sku, name, qty_left, unit, picture, category FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))
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

			{"sku":item[0],
			"name": item[1],
			"remaining": item[2],
			"unit": item[3],
			"starting": initial_quantity,
			"recieved": recieved,
			"demand": delivered_out,
			"picture": item[4].encode('ascii'),
			"category": item[5].encode('ascii')
			})
		
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
		things.append({"name": row[0].encode('ascii'),
			"dateTime": row[1],
			"action":row[2],
			"move":row[3],
			"remaining":row[4],
			"item":row[5].encode('ascii'),
			"location":row[6]})
		# print(things)
			
	return things
		

# Returns inventory items that are below threshold levels
def getInventoryLow():

	THRESHOLD = 1.2
	cursor = mysql.connect().cursor()
	cursor.execute("""SELECT sku, name, qty_left, reorder_pt, picture, category FROM Ascott_InvMgmt.Items
		WHERE qty_left <= '"""+str(THRESHOLD)+"""'*reorder_pt
		ORDER BY name ASC;""")
	data = cursor.fetchall()

	r = []
	for i in data:
		r.append({"sku": i[0],
			"name": i[1].encode('ascii'),
			"qty_left": i[2],
			"reorder_pt": i[3],
			"picture": i[4].encode('ascii'),
			"category": i[5].encode('ascii')})
		
	return r

def getDailyLogs():

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(
		"SELECT user, date_time, action, qty_moved, qty_left, item, location FROM Ascott_InvMgmt.Logs WHERE day(date_time) = day(now());")
	data=cursor.fetchall()
	things = []
	
	for row in data:
		things.append({"name": row[0].encode('ascii'),
			"dateTime": row[1],
			"action":row[2],
			"move":row[3],
			"remaining":row[4],
			"item":row[5].encode('ascii'),
			"location":row[6]})
		print(things)
			
	return things

# POST for getting chart data
@app.route('/api/getChartData', methods=["POST"])
def getChartData():

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
	if u'logged_in' in session:
		return session['logged_in']
	return False

# wrapper function for route redirection
def filter_role(roles_routes):
	for k,v in roles.items():
		if session['role'] == k:
			return redirect(v)


@app.template_filter('lang_strip')
def lang_strip(s):
    l = re.search(r"(?m)(?<=(en\/)|(zh\/)|(ms\/)|(ta\/)).*$", str(s.encode('ascii')))
    if l:
        return l.group()
    return None

# case query for mobile input
def input_handler(qty, user):
	query = 'UPDATE Items SET qty_left = CASE WHEN action'


@app.before_request
def before():
	# localization setting
	if request.view_args and 'lang_code' in request.view_args:
	    if request.view_args['lang_code'] not in languages:
	    	g.current_lang = "en" # default localisation
	        # return abort(404)
	    else:
	    	g.current_lang = request.view_args['lang_code']
	    	session["lang_code"] = g.current_lang
	    	request.view_args.pop('lang_code')

	# user authentication
	if u'logged_in' not in session:
		session["logged_in"] = False


@babel.localeselector
def get_locale():
    return g.get('current_lang', 'en')


##########################
##        ROUTES        ##
##########################


@app.route('/')
def hello():
	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))
	else:
		# user already logged_in previously
		if session['role'] == "supervisor":
			return redirect(url_for("dashboard", lang_code=session["lang_code"]))
		elif session['role'] == "attendant":
			return redirect(url_for("scanner", lang_code=session["lang_code"]))

@app.route('/<lang_code>/login', methods=["GET", "POST"])
def login():
	
	# create a login form to collect username & password
	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else: 
			username = form.username.data
			password = form.password.data
			remember = form.remember.data
		
			cursor = mysql.connect().cursor()
			cursor.execute("SELECT username, password, role, name FROM User WHERE username= '" + username + "';")

			# check if user and pass data is correct by executing the db
			# data is stored as a tuple
			data = cursor.fetchone()
	
			if data is None: 
				# username does not match records
				flash('User does not exist')
				return redirect(url_for("login", lang_code=get_locale()))

			elif password != data[1]:
				# password does not match records
				flash('Incorrect password')
				return redirect(url_for("login", lang_code=get_locale()))

			else:
				# username & password match
				session['username'] = data[0]
				session['role'] = data[2]
				session['name'] = data[3]
				session['logged_in'] = True
				if remember:
					session.permanent = True

				# check role
				if data[2] == "supervisor":
					return redirect(url_for("dashboard", lang_code=get_locale()))
				elif data[2] =="attendant":
					return redirect(url_for("scanner", lang_code=get_locale()))

	elif request.method == "GET":

		# user authentication
		if not session["logged_in"]:
			return render_template("login.html", form=form)
		else:
			# user already logged_in previously
			if session['role'] == "supervisor":
				return redirect(url_for("dashboard", lang_code=get_locale()))
			elif session['role'] == "attendant":
				return redirect(url_for("scanner", lang_code=get_locale()))


@app.route('/<lang_code>/admin', methods=["GET","POST"])
def admin():

	form = AddUserForm()
	if request.method=="POST":
		if form.validate == False:
			return render_template('admin.html', form=form)
		else:
			username=form.username.data
			password=form.password.data
			role=form.role.data
			name=form.name.data

			newuser=[username,password,role,name]
			

			conn = mysql.connect()
			cursor = conn.cursor()

			# TODO: string parameterisation
			query = "INSERT INTO User VALUES ('{}','{}','{}','{}'); COMMIT".format(newuser[0],newuser[1],newuser[2],newuser[3])

			# query = "INSERT INTO User (username,password,role,name) VALUES ();"

			cursor.execute(query)
			# cursor.execute("COMMIT")
			return "congrats"

			


	elif request.method =="GET":
		if not session["logged_in"]:
			return redirect(url_for("login", lang_code=session["lang_code"]))
		else:
			return render_template('admin.html', form=form)



@app.route('/<lang_code>/dashboard')
def dashboard():

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect(url_for("login", lang_code=get_locale()))

	i = getInventoryLow()
	l = getDailyLogs()
	# l = getLogs()

	return render_template('dashboard.html', items = i, logs = l)



@app.route('/<lang_code>/inventory')
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
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))
			
	# get current list of all items listed in db
	supplies = getAllInventory('Guest Supplies')
	hampers = getAllInventory('Guest Hampers')
	kitchenware = getAllInventory('Kitchenware')
	return render_template('v2/inventory.html',
		supplies = supplies,
		hampers = hampers,
		kitchenware = kitchenware)

@app.route('/<lang_code>/inventory/<int:sku>')
def item(sku):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	name = item
	cursor = mysql.connect().cursor()

	query = "SELECT name, category, picture, location FROM Ascott_Invmgmt.Items WHERE sku = '{}';".format(sku)
	cursor.execute(query)
	data = cursor.fetchall()
	d = [[s.encode('ascii') for s in list] for list in data]

	r = []
	for i in data:
		r.append({"name": i[0].encode('ascii'),
			"category": i[1].encode('ascii'),
			"picture": i[2].encode('ascii'),
			"location": i[3].encode('ascii')})

	# print d
	try:
		return render_template('v2/item.html', item = r)
	except:
		return render_template('v2/item.html', item = None)

@app.route('/<lang_code>/review/<category>')
def category(category):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	category = category
	itemtype = getAllInventory(category)
	return render_template('v2/category.html', category=category, itemtype=itemtype, 
		role = role,
		user = session['username'])


@app.route('/<lang_code>/review')
def review():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	supplies = getAllInventory('Guest Supplies')
	hampers = getAllInventory('Guest Hampers')
	kitchenware = getAllInventory('Kitchenware')
	return render_template('review.html', supplies = supplies,
		hampers = hampers,
		kitchenware = kitchenware, user=session['username'])

# @app.route('/review')
# def review():
# 	supplies = getAllInventory('Guest Supplies')
# 	hampers = getAllInventory('Guest Hampers')
# 	kitchenware = getAllInventory('Kitchenware')
# 	return render_template('v2/review.html', supplies = supplies,
# 		hampers = hampers,
# 		kitchenware = kitchenware, user=session['username'])
# >>>>>>> b1fcaf40dc6f258ef881c7d5b27fa57d50f88415


@app.route('/<lang_code>/logs')
def logs():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	logs=getAllLogs()
	# names=getUniqueNames()
	# items=getUniqueItems()
	return render_template('v2/logs.html',
		logs=logs, 
		role = role,
		user = session['username'])
	# names=names, items=items)

@app.route('/<lang_code>/scan')
def scanner():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	return render_template('scanner.html')

# RA shelf view
@app.route('/<lang_code>/shelves/<tag_id>/', methods=['GET', 'POST'])
# @cache.cached(timeout=50)
def shelf(tag_id):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	if request.method == 'POST':
		now = datetime.now()
		form_data = request.form
		user = session['username']

		print(form_data)
		return hello()
		
		# conn = mysql.connect()
		# cursor = conn.cursor()
		# for item, qty in form_data.iteritems():
		# 	cursor.execute("SELECT qty_left FROM Items WHERE sku="+item+" AND location="+tag_id+";")
		# 	qty_left = cursor.fetchone()[0]  - qty
		# 	if (qty_left > 0):
		# 		# query for stock out
		# 		print("UPDATE Items SET qty_left = qty_left-"+qty+" WHERE qty_left >= "+qty+" AND sku="+item+" AND location="+tag_id+";")
		# 		# create log for each item
		# 		print("INSERT INTO Logs (user, date_time, action, qty_moved, qty_left, name, location) VALUES ({}, {}, 'out', {}, {}, {});".format(user, now, qty, qty_left, item, tag_id))
		# 	else:
		# 		flash('Not enough in store!')

		# return redirect('/scan')

	else:

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
# <<<<<<< HEAD
# 	else:
# 		return redirect(url_for("scan", lang_code=get_locale()))


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
# =======
	
# >>>>>>> ce4495d2f9e2602556e384a44cb683e0df1c27ad

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("login", lang_code=get_locale()))


@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, nothing at this URL.', 404


## testing
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')