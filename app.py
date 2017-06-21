from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, g
from flask_babel import Babel
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from forms import LoginForm, RetrievalForm, AddUserForm, CreateNewItem,AddNewLocation
import os, copy, re, csv, json_decode
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
		"SELECT sku, name, qty_left, reorder_pt, unit, picture, category FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))
	data = cursor.fetchall()
	items = []
	for item in data:
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
		remaining_quantity = item[2]
		initial_quantity = remaining_quantity + delivered_out - received
		items.append(

			{"sku":item[0],
			"name": item[1],
			"remaining": item[2],
			"reorder": item[3],
			"unit": item[4],
			"starting": initial_quantity,
			"received": received,
			"demand": delivered_out,
			"picture": item[5].encode('ascii'),
			"category": item[6].encode('ascii')
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
	    page_not_found(400)
	else:
		conn = mysql.connect()
		cursor = conn.cursor()

		# TODO: string parameterisation
		query = "SELECT sku FROM Ascott_InvMgmt.Items WHERE name = '{}';".format(request.json)

		cursor.execute(query)
		idItem = cursor.fetchone()[0]
		# print(idItem)

		# query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = {0}".format(idItem)
		query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = 1"
		# TODO: string parameterisation
		# query = "SELECT datetime, qtyAfter FROM Ascott_InvMgmt.Logs WHERE idItem = {}".format(idItem)
		cursor.execute(query)
		responseData = cursor.fetchall()

		return jsonify(responseData)

# POST for getting chart data
@app.route('/api/editReorder', methods=["POST"])
def editReorder():

	print "content_type: ", request.content_type
	print "request.json: ", request.json

	data = request.get_json()
	# print(data, type(data))
	# print(json_decode.json_loads_byteified(data), type(json_decode.json_loads_byteified(data)))
	new_reorder = int(data[u"qty"])
	name = data[u"name"].encode('ascii')
	print(new_reorder, name)

	if not request.json:
	    print "Bad json format"
	    page_not_found(400)
	else:
		cursor = mysql.connect().cursor()

		# TODO: string parameterisation
		query = "UPDATE Ascott_InvMgmt.Items SET reorder_pt={} WHERE (name='{}' AND sku > 0);".format(new_reorder, name)
		print query
		cursor.execute(query)
		idItem = cursor.fetchone()
		print(idItem)

		# # query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = {0}".format(idItem)
		# query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = 1"
		# # TODO: string parameterisation
		# # query = "SELECT datetime, qtyAfter FROM Ascott_InvMgmt.Logs WHERE idItem = {}".format(idItem)
		# cursor.execute(query)
		# responseData = cursor.fetchall()

		return jsonify(data)

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


@app.route('/<lang_code>/admin', methods=["GET","POST"])
def admin():

	form = AddUserForm()
	form2 = CreateNewItem()
	form3 =AddNewLocation()

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

	cursor.execute("SELECT location FROM Ascott_InvMgmt.Items;")

	data1 = cursor.fetchall()
	data2 = list(set(list(data1))) #displays all unique NFC id tags.
	
	NFCs=[]
	group={}
	items=[]
	

	for idNFC in data2:
		NFCs.append(
			{"NFC": idNFC[0].encode('ascii')})
	
	for i in NFCs:
		 
		val = i['NFC'] #details of NFC location 

		#fetch all item names pertaining to the tag.
		cursor.execute("SELECT name FROM Ascott_InvMgmt.Items WHERE location = '{}';".format(val))
		data3=cursor.fetchall()
		
		group[val] = data3


	if request.method =="GET":

		# user authentication
		if not session["logged_in"]:
			return redirect(url_for("login", lang_code=session["lang_code"]))

		cursor.execute("SELECT DISTINCT name FROM Ascott_InvMgmt.Items;")
		items = cursor.fetchall()
		# print (items)
		flat_items = [item.encode('ascii') for sublist in items for item in sublist]
		return render_template('v2/admin.html', form=form, form2=form2,form3=form3, users=things, group=group, item_list=flat_items)

	

	elif request.method == "POST":

		if request.form['name-form'] =='form':
			if form.validate() == False:
				return render_template('admin.html', form=form, form2=form2,form3=form3, users=things, group=group)
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
				flash("User is added!")
				return redirect(url_for('admin', lang_code=get_locale()))

		elif request.form['name-form'] =='form2':
			if form2.validate() == False:
				return render_template('admin.html', form=form, form2=form2,form3=form3, users=things, group=group)
			else: 
				sku = form2.sku.data

				

				# query1 = "SELECT itemname,reorderpt,batchqty,category,picture,unit FROM Ascott_InvMgmt.Items WHERE sku ='{}'".format(sku))

				itemname=form2.itemname.data
				location=form2.location.data
				qtyleft=form2.qtyleft.data
				reorderpt=form2.reorderpt.data
				batchqty=form2.batchqty.data
				category=form2.category.data
				picture=form2.picture.data
				unit=form2.unit.data

				newitem=[sku,itemname,location,qtyleft,reorderpt,batchqty,category,picture,unit]

				conn = mysql.connect()
				cursor = conn.cursor()

				# TODO: string parameterisation
				query = "INSERT INTO Items VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}'); COMMIT".format(newitem[0],newitem[1],newitem[2],newitem[3],newitem[4],newitem[5],newitem[6],newitem[7],newitem[8])
	
				cursor.execute(query)
				# cursor.execute("COMMIT")
				flash("New item is added!")
				return redirect(url_for('admin', lang_code=get_locale()))

		elif request.form['name-form'] =='form3':
			if form3.validate() == False:
				return render_template('admin.html', form=form, form2=form2,form3=form3, users=things, group=group)
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
	query = "SELECT name, category, picture, location, qty_left, reorder_pt, batch_qty, unit FROM Ascott_InvMgmt.Items WHERE sku = '{}';".format(sku)
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
			"unit": i[7].encode('ascii')})

	# print d
	print r
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
		role = session['role'],
		user = session['username'])


# @app.route('/<lang_code>/review')
# def review():

# 	# user authentication
# 	if not session["logged_in"]:
# 		return redirect(url_for("login", lang_code=session["lang_code"]))

# 	supplies = getAllInventory('Guest Supplies')
# 	hampers = getAllInventory('Guest Hampers')
# 	kitchenware = getAllInventory('Kitchenware')
# 	return render_template('review.html', supplies = supplies,
# 		hampers = hampers,
# 		kitchenware = kitchenware, user=session['username'])

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
		role = session['role'],
		user = session['username'])
	# names=names, items=items)

@app.route('/<lang_code>/scan')
def scanner():

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	return render_template('scanner.html')

# RA shelf view
@app.route('/<lang_code>/shelves/<tag_id>', methods=['GET'])
def shelf(tag_id):

	# user authentication
	if not session["logged_in"]:
		return redirect(url_for("login", lang_code=session["lang_code"]))

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT sku, name, category, picture FROM Items WHERE location = '{}';".format(tag_id))

	data=cursor.fetchall()
	things = []
	for item in data:
		things.append(
			{"sku":item[0],
			"name": item[1],
			"category": item[2],
			"picture":item[3]})
	return render_template('storeroom.html', things=things, 
		role = session['role'],
		user = session['username'], 
		location = tag_id)

@app.route('/<lang_code>/shelves/<tag_id>/cart', methods=['POST'])
def processCart(tag_id):
	now = datetime.now()
	form_data = request.form
	user = session['username']
	
	conn = mysql.connect()
	cursor = conn.cursor()
	for item, qty in form_data.iteritems():
		print(item)
		print(qty)
		cursor.execute("SELECT qty_left FROM Items WHERE sku="+item+" AND location='"+tag_id+"';")
		# if action == 'out':
		# 	qty_left = cursor.fetchone()[0]  - qty
		# 	if (qty_left > 0):
		# 		# query for stock out
		# 		print("UPDATE Items SET qty_left="+qty_left+" WHERE qty_left>="+qty+" AND sku="+item+" AND location='"+tag_id+"';")
		# 		# create log for each item
		# 		print("INSERT INTO Logs (user, date_time, action, qty_moved, qty_left, name, location) VALUES ({}, {}, 'out', {}, {}, {});".format(user, now, qty, qty_left, item, tag_id))
		# 	else:
		# 		flash('Not enough in store!')
		message = 'feedback'

	return redirect('shelves/'+tag_id, message=message)

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