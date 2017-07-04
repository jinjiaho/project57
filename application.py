from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, g
from flask_babel import Babel
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from forms import LoginForm, RetrievalForm, AddUserForm, CreateNewItem,AddNewLocation,ExistingItemsLocation
import os, copy, re, csv, json_decode
# from flask.ext.cache import Cache


# pip2 install flask
# pip2 install mysql-python
# pip2 install mysqlclient
# pip2 install SQLAlchemy
# pip2 install flask-babel
# pip2 install flask-wtf
# pip2 install flask-mysql
# pip2 install numpy
# pip2 install scipy
# pip2 install statsmodels
# pip2 install pandas
# eb init -p python2.7 aim
# eb init
# eb create flask-env
# eb open
# eb terminate flask-env

##########################
##        CONFIG        ##
##########################
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

application = Flask(__name__, instance_relative_config=True)
# application.config.from_object('config.DevConfig') # default configurations
application.config.from_pyfile('amazonRDS.cfg') # override with instanced configuration (in "/instance"), if any
# application.config.from_pyfile('myConfig1.cfg')
# application.config.from_pyfile('myConfig2.cfg')

# Babel init
babel = Babel(application)
languages = ('en', 'zh', 'ms', 'ta')

# mysql init
mysql = MySQL()
mysql.init_app(application)

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
		"SELECT iid, name, qty_left, reorder_pt, unit, picture, category, price FROM Ascott_InvMgmt.view_item_locations WHERE category = '{}';".format(category))
	data = cursor.fetchall()

	# cursor.execute(
	# 	"SELECT DISTINCT iid FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))
	# unique_iid = cursor.fetchall()
	# print(unique_iid)
	items = []
	counter = 0
	for item in data:
		if item[0] == counter:
			pass
		else:
			cursor.execute(
			"SELECT action, qty_moved FROM Ascott_InvMgmt.Logs WHERE month(date_time) = month(now()) AND year(date_time) = year(now()) AND item='{}';".format(item[0]))
			in_out_data = cursor.fetchall()
			delivered_out = 0
			received = 0
			for i in in_out_data:
				if i[0].encode('ascii') == 'out':
					delivered_out = delivered_out + (-1*int(i[1]))
				elif i[0].encode('ascii') == "in":
					received = received + int(i[1])
			value_in = received*item[7]
			value_out = delivered_out*item[7]

			cursor.execute(
			"SELECT qty_left FROM Ascott_InvMgmt.view_item_locations WHERE iid='{}';".format(item[0]))
			location_qty = cursor.fetchall()
			remaining_quantity = 0
			for i in location_qty:
				remaining_quantity += i[0]
			initial_quantity = remaining_quantity + delivered_out - received
			items.append(

				{"iid":item[0],
				"name": item[1],
				"remaining": remaining_quantity,
				"reorder": item[3],
				"unit": item[4],
				"starting": initial_quantity,
				"received": received,
				"demand": delivered_out,
				"picture": item[5].encode('ascii'),
				"category": item[6].encode('ascii'),
				"value_in": value_in,
				"value_out": value_out,
				"price": item[7]
				})
			counter = item[0]

	return items

# Returns all the items based on location. KIV for possible supervisor view filtering.
def getFromLevels(location):
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT name, category, location FROM Ascott_InvMgmt.view_item_locations WHERE location = '{}';".format(location))

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
		cursor.execute(
			"SELECT name FROM Ascott_InvMgmt.Items WHERE iid  = '{}';".format(row[5]))
		item_name = cursor.fetchall()

		print(row[0])



		things.append({"name": row[0].encode('ascii'),
			"dateTime": row[1],
			"action":row[2],
			"move":row[3],
			"remaining":row[4],
			"item":item_name[0][0].encode('ascii'),
			"location":row[6]})
		# print(things)

	return things


# Returns inventory items that are below threshold levels
def getInventoryLow():

	THRESHOLD = 1.2
	cursor = mysql.connect().cursor()
	cursor.execute("""SELECT iid, name, qty_left, reorder_pt, picture, category FROM Ascott_InvMgmt.view_item_locations
		WHERE qty_left <= '"""+str(THRESHOLD)+"""'*reorder_pt AND
		qty_left > 0
		ORDER BY name ASC;""")
	data = cursor.fetchall()

	r = []
	for i in data:
		r.append({"iid": i[0],
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
@application.route('/api/getChartData', methods=["POST"])
def getChartData():

	print "content_type: ", request.content_type
	print "request.json: ", request.json

	data = str(request.get_json())
	# print(data, type(data))

	if not request.json:
	    print "Bad json format"
	    page_not_found(400)
	else:
		conn = mysql.connect()
		cursor = conn.cursor()

		# TODO: string parameterisation
		query = "SELECT iid FROM Ascott_InvMgmt.Items WHERE name = '{}';".format(request.json)

		cursor.execute(query)
		idItem = cursor.fetchone()[0]
		# print(idItem)

		query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = {}".format(idItem)
		# query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = 1"
		# TODO: string parameterisation
		cursor.execute(query)
		responseData = cursor.fetchall()

		return jsonify(responseData)

# POST for getting chart data
@application.route('/api/editReorder', methods=["POST"])
def editReorder():

	print "content_type: ", request.content_type
	print "request.json: ", request.json

	data = request.get_json()

	if data["tracking"] == u"off" or (data["qty"] == u"" or data["qty"] == u"0"):
		print("no qty specified")
		new_reorder = 0
	else:
		new_reorder = int(data[u"qty"])
	name = data["name"].encode('ascii')


	if not request.json:
	    print "Bad json format"
	    page_not_found(400)
	else:
		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.execute(
			"UPDATE Ascott_InvMgmt.Items SET reorder_pt=%s WHERE (name=%s AND iid > 0);",
			(new_reorder, name))
		conn.commit()
		# idItem = cursor.fetchone()

		# # query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = {0}".format(idItem)
		# query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = 1"
		# # TODO: string parameterisation
		# # query = "SELECT datetime, qtyAfter FROM Ascott_InvMgmt.Logs WHERE idItem = {}".format(idItem)
		# cursor.execute(query)
		# responseData = cursor.fetchall()

		return jsonify("")

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


@application.template_filter('lang_strip')
def lang_strip(s):
    l = re.search(r"(?m)(?<=(en\/)|(zh\/)|(ms\/)|(ta\/)).*$", str(s.encode('ascii')))
    if l:
        return l.group()
    return None

# case query for mobile input
def input_handler(qty, user):
	query = 'UPDATE Items SET qty_left = CASE WHEN action'


@application.before_request
def before():
	# localization setting
	if request.view_args and 'lang_code' in request.view_args:
	    if request.view_args['lang_code'] not in languages:
	    	g.current_lang = "en" # default localisation
	    else:
	    	g.current_lang = request.view_args['lang_code']
	    	session["lang_code"] = g.current_lang
	    	request.view_args.pop('lang_code')
	else:
		session["lang_code"] = "en" # default localisation
		g.current_lang = "en"

	# user authentication
	if u'logged_in' not in session:
		session["logged_in"] = False


@babel.localeselector
def get_locale():
    return g.get('current_lang', 'en')


##########################
##        ROUTES        ##
##########################


@application.route('/')
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

@application.route('/<lang_code>/login', methods=["GET", "POST"])
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

			# elif password != hashpass:
			elif check_password_hash(data[1],password) ==False:
				# password does not match records
				flash('Incorrect password')
				return redirect(url_for("login", lang_code=get_locale()))

			else:
				# username & password match
				print(data[2])
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

	else:
		return redirect(url_for("hello"))


@application.route('/<lang_code>/admin', methods=["GET","POST"])
def admin():

	form = AddUserForm()
	form2 =CreateNewItem()
	form3 =AddNewLocation()
	form4 =ExistingItemsLocation()

	#--------------users table-------------------------
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT role, name FROM Ascott_InvMgmt.User;")

	data = cursor.fetchall()
	# print(data)
	things = []
	for item in data:
		things.append(
			{"role": item[0],
			"name": item[1]})

#-------------NFCID----------------------------------

	cursor.execute("SELECT DISTINCT location FROM Ascott_InvMgmt.TagItems;")

	data1 = cursor.fetchall() #displays all unique NFC id tags.

	NFCs=[]
	group={}
	items=[]


	for idNFC in data1:
		NFCs.append(idNFC[0].encode('ascii'))

	for i in NFCs:

		#fetch all item names pertaining to the tag.
		cursor.execute("SELECT name, iid FROM Ascott_InvMgmt.view_item_locations WHERE location = '{}';".format(i))
		data3=cursor.fetchall()

		group[i] = data3


	if request.method =="GET":

		# user authentication
		if not session["logged_in"]:
			return redirect(url_for("login", lang_code=session["lang_code"]))

		cursor.execute("SELECT DISTINCT name FROM Ascott_InvMgmt.Items;")
		items = cursor.fetchall()
		# print (items)
		flat_items = [item.encode('ascii') for sublist in items for item in sublist]
		return render_template('admin.html',
			form=form,
			form2=form2,
			form3=form3,
			form4=form4,
			users=things,
			group=group,
			item_list=flat_items)


	elif request.method == "POST":

		if request.form['name-form'] =='form':
			if form.validate() == False:
				return render_template('admin.html',
					form=form,
					form2=form2,
					form3=form3,
					form4=form4,
					users=things,
					group=group)
			else:
				username = form.username.data
				password = generate_password_hash(form.password.data)
				role = form.role.data
				name = form.name.data

				newuser=[username,password,role,name]


				conn = mysql.connect()
				cursor = conn.cursor()

				# TODO: string parameterisation
				query = "INSERT INTO User VALUES ('{}','{}','{}','{}'); COMMIT".format(newuser[0],newuser[1],newuser[2],newuser[3])

				# query = "INSERT INTO User (username,password,role,name) VALUES ();"

				cursor.execute(query)
				# cursor.execute("COMMIT")
				flash("User has been added!")
				return redirect(url_for('admin', lang_code=get_locale()))

		elif request.form['name-form'] =='form2':
			if form2.validate() == False:
				return render_template('admin.html',
					form=form,
					form2=form2,
					form3=form3,
					form4=form4,
					users=things,
					group=group)
			else:
				iid = form2.iid.data

				# query1 = "SELECT itemname,reorderpt,batchqty,category,picture,unit FROM Ascott_InvMgmt.Items WHERE iid ='{}'".format(iid))

				itemname = form2.itemname.data
				# location = form2.location.data
				# qtyleft = form2.qtyleft.data
				reorderpt = form2.reorderpt.data
				batchqty = form2.batchqty.data
				category = form2.category.data
				picture = form2.picture.data
				unit = form2.unit.data
				price = 0.0000 # TODO: CREATE FORM FIELD FOR PRICE

				# newitem = [iid, itemname, reorderpt, batchqty, category, picture, unit]

				# TODO: string parameterisation
				conn = mysql.connect()
				cursor = conn.cursor()

				query = "INSERT INTO Items (name, reorder_pt, batch_qty, category, picture, unit, price) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}'); COMMIT".format(itemname, reorderpt, batchqty, category, picture, unit, price)

				cursor.execute(query)
				# cursor.execute("COMMIT")
				flash("New item is added!")
				return redirect(url_for('admin', lang_code=get_locale()))

		elif request.form['name-form'] =='form3':
			if form3.validate() == False:
				return render_template('admin.html',
					form=form,
					form2=form2,
					form3=form3,
					form4=form4,
					users=things,
					group=group)
			else:
				location = form3.location.data
				description= form3.description.data

				newlocation = [location,description]

				conn = mysql.connect()
				cursor = conn.cursor()

				# TODO: string parameterisation
				query = "INSERT INTO LocationInfo VALUES ('{}','{}'); COMMIT".format(newlocation[0],newlocation[1])

				cursor.execute(query)
				# cursor.execute("COMMIT")
				flash("New Location is Added!")

				return redirect(url_for('admin', lang_code=get_locale()))

		elif request.form['name-form'] =='form4':
			if form4.validate() == False:
				return render_template('admin.html',
					form=form,
					form2=form2,
					form3=form3,
					form4=form4,
					users=things,
					group=group)
			else:
				itemname = form4.itemname.data
				# qtyleft= form4.qtyleft.data
				# location=form4.location.data
				price = 0.0000

				newEntries = [itemname,qtyleft,location]

				conn = mysql.connect()
				cursor = conn.cursor()

				cursor.execute("SELECT iid,reorder_pt,batch_qty,category,picture,unit FROM Ascott_InvMgmt.Items WHERE name = '{}';".format(itemname))

				info = cursor.fetchall()

				listing=[]
				for i in info:
					for j in i:
						listing.append(j)

				listing.insert(1,itemname)
				listing.append(price)
				# listing.insert(2,location)
				# listing.insert(3,qtyleft)

				# TODO: string parameterisation
				query = "INSERT INTO Items (name, reorder_pt, batch_qty, category, picture, unit, price) VALUES ('{}','{}','{}','{}','{}','{}','{}'); COMMIT".format(listing[1],listing[2],listing[3],listing[4],listing[5],listing[6],listing[7])

				cursor.execute(query)
				flash("Added Item to Location %s!" %location)

				return redirect(url_for('admin', lang_code=get_locale()))


@application.route('/<lang_code>/dashboard')
def dashboard():

	# user authentication
	logged_in = auth()
	if not logged_in:
		return redirect(url_for("login", lang_code=get_locale()))

	i = getInventoryLow()
	l = getDailyLogs()
	# l = getLogs()

	return render_template('dashboard.html', 
		role=session['role'], 
		user=session['username'], 
		items = i, 
		logs = l)



@application.route('/<lang_code>/inventory')
def inventory():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	cursor = mysql.connect().cursor()
	cursor.execute("SELECT DISTINCT category FROM Items;")
	data = cursor.fetchall()
	categories = []
	for c in data:
		categories.append(getAllInventory(c[0].encode('ascii')))

	# supplies = getAllInventory('Guest Supplies')
	# hampers = getAllInventory('Guest Hampers')
	# kitchenware = getAllInventory('Kitchenware')

	# get list of all locations to display
	location_query = "SELECT DISTINCT location FROM view_item_locations GROUP BY location DESC;"
	cursor = mysql.connect().cursor()
	cursor.execute(location_query)
	locations = cursor.fetchall()
	shelves = []
	for i in locations:
		# print type(i[0])
		shelves.append(i[0].encode('ascii'))

	

	return render_template('inventory.html',
		user = session['username'],
		role = session['role'],
		categories = categories,
		num_cat = len(categories),
		shelves = shelves)


@application.route('/<lang_code>/inventory/<int:iid>', methods=['GET', 'POST'])
def item(iid):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	
	# name = item


	# name = item

	cursor = mysql.connect().cursor()
	query = "SELECT name, category, picture, location, qty_left, reorder_pt, batch_qty, unit, price FROM Ascott_InvMgmt.view_item_locations WHERE iid = '{}';".format(iid)
	cursor.execute(query)
	data = cursor.fetchall()
	# d = [[s.encode('ascii') for s in list] for list in data]

	r = []
	for i in data:
		r.append({"name": i[0].encode('ascii'),
			"category": i[1].encode('ascii'),
			"picture": i[2].encode('ascii'),
			"location": i[3].encode('ascii'),
			"qty_left": i[4],
			"reorder": i[5],
			"batch_size": i[6],
			"unit": i[7].encode('ascii'),
			"price": i[8]})


	print r

	cursor.execute("SELECT new_price, date_effective FROM Ascott_InvMgmt.pricechange WHERE item = '{}';".format(iid))
	price = cursor.fetchall()
	pricechanges = []
	if price == ():
		pricechanges.append({
			"new_price": 0,
			"date_effective": 0})
	else:
	
		for item in price:
			pricechanges.append({
				"new_price": item[0],
				"date_effective": item[1]})

	try:
		return render_template('item.html', item = r, pricechanges = pricechanges)
	except:
		return render_template('item.html', item = None, pricechanges = None)


@application.route('/<lang_code>/review/<category>')
def category(category):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	category = category
	itemtype = getAllInventory(category)
	return render_template('category.html',
		category=category,
		itemtype=itemtype,
		role = session['role'],
		user = session['username'])



@application.route('/<lang_code>/logs')
def logs():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	logs=getAllLogs()
	# names=getUniqueNames()
	# items=getUniqueItems()
	return render_template('logs.html',
		logs=logs,
		role = session['role'],
		user = session['username'])
	# names=names, items=items)

@application.route('/<lang_code>/scan')
def scanner():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	return render_template('scanner.html')

# RA shelf view
@application.route('/<lang_code>/shelves/<tag_id>', methods=['GET', 'POST'])
def shelf(tag_id):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT iid, name, category, picture FROM view_item_locations WHERE location = '{}';".format(tag_id))

	data=cursor.fetchall()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
	things = []
	for item in data:
		things.append(
			{"iid":item[0],
			"name": item[1],
			"category": item[2],
			"picture":item[3]})
	message = ''

	# get permissions for user
	# cursor.execute("SELECT stock_in, admin FROM Permissions WHERE role='{}'".format(session['role']))
	# permissions = cursor.fetchall()[0][0]
	# print(permissions)

	if request.method == 'POST':
		now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		form_data = request.form
		user = session['username']

		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			for item, info in form_data.iterlists():
				print(item)
				print(info[0]+", "+info[1])
				cursor.execute("SELECT qty_left FROM view_item_locations WHERE iid="+item+" AND location='"+tag_id+"';")
				conn.commit()
				old_qty = cursor.fetchone()[0]
				qty_input = int(info[0])
				if info[1] == 'out':
					qty_left = old_qty  - qty_input
					qty_input = qty_input * (-1) 	# make qty_input negative to reflect taking qty OUT of store.

					if qty_left < 0:
						flash('Not enough in store!', 'warning')

				elif info[1] == 'in':
					qty_left = old_qty + qty_input
				else:
					qty_left = qty_input
					qty_input = qty_left - old_qty # change the value of qty to the difference
				conn = mysql.connect()
				cursor = conn.cursor()
				update_items_query = "UPDATE TagItems SET qty_left="+str(qty_left)+" WHERE iid="+str(item)+" AND location='"+tag_id+"';"
				# message += update_items_query
				# query for stock out
				print(update_items_query)
				cursor.execute(update_items_query)
				conn.commit()
				conn = mysql.connect()
				cursor = conn.cursor()
				update_logs_query = "INSERT INTO Logs (user, date_time, action, qty_moved, qty_left, item, location) VALUES ('{}', '{}', '{}', {}, {}, {}, '{}');".format(user, now, info[1], qty_input, qty_left, item, tag_id)
				# message += " " + update_logs_query
				# create log for each item
				print(update_logs_query)
				cursor.execute(update_logs_query)
				conn.commit()
			flash('Success!', 'success')
		except:
			flash('Oops! Something went wrong :(', 'danger')

	return render_template('storeroom.html', things=things,
		role = session['role'],
		user = session['username'],
		location = tag_id)


@application.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("login", lang_code=get_locale()))


@application.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, nothing at this URL.', 404


## testing
if __name__ == '__main__':
	application.run()
