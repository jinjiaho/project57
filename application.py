from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, g
from flask_babel import Babel
from flask_uploads import UploadSet, IMAGES, configure_uploads
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
application.config.from_object('config.DevConfig') # default configurations
# application.config.from_pyfile('amazonRDS.cfg') # override with instanced configuration (in "/instance"), if any
application.config.from_pyfile('myConfig1.cfg')
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

# Configure the image uploading via Flask-Uploads
photos = UploadSet('images', IMAGES)
configure_uploads(application, photos)


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
    #   "SELECT DISTINCT iid FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))
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

# Quick query for inventory for mobile and web Inventory views.
# Called by inventory() and shelf()
# If location is None, we can infer that user has admin rights, and can therefore see the qty left.
def inventoryQuick(location):
    items = []
    cursor = mysql.connect().cursor()
    if location == None:
        cursor.execute("SELECT iid, name, category, picture, SUM(qty_left), reorder_pt FROM view_item_locations GROUP BY iid;")
        data = cursor.fetchall()
        for d in data:
            items.append(
                {"iid":d[0],
                "name": d[1].encode('ascii'),
                "category": d[2].encode('ascii'),
                "picture": d[3].encode('ascii'),
                "remaining": d[4],
                "reorder": d[5]
                })
    else:
        cursor.execute("SELECT iid, name, category, picture FROM view_item_locations WHERE location='{}' AND reorder_pt >= 0;".format(location))
        data = cursor.fetchall()
        for d in data:
            items.append(
                {"iid":d[0],
                "name": d[1].encode('ascii'),
                "category": d[2].encode('ascii'),
                "picture":d[3].encode('ascii')
                })
    return items

# Stock Update Function for RA, Runner and Supervisors.
# Called by item() and shelf().
# Returns True if the stock was updated successfully, False otherwise.
def stockUpdate(iid, location, inputQty, user, action, time):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT qty_left FROM view_item_locations WHERE iid={} AND location='{}';".format(iid, location))
        data = cursor.fetchall()
        old_qty = data[0][0]
        print(old_qty)
        if action == 'out':
            qty_left = old_qty  - inputQty
            qty_diff = inputQty * (-1)     # make qty_input negative to reflect taking qty OUT of store.

            if qty_left < 0:
                flash('Not enough in store!', 'warning')

        elif action == 'in':
            qty_left = old_qty + inputQty
            qty_diff = qty
        else:
            qty_left = inputQty
            qty_diff = qty_left - old_qty # change the value of qty to the difference
        conn = mysql.connect()
        cursor = conn.cursor()
        update_items_query = "UPDATE TagItems SET qty_left={} WHERE iid={} AND location='{}';".format(qty_left, iid, location)

        # general query for all actions
        print(update_items_query)
        cursor.execute(update_items_query)
        conn.commit()

        # Log action
        conn = mysql.connect()
        cursor = conn.cursor()
        update_logs_query = "INSERT INTO Logs (user, date_time, action, qty_moved, qty_left, item, location) VALUES ('{}', '{}', '{}', {}, {}, '{}', '{}');".format(user, time, action, qty_diff, qty_left, iid, location)
        print(update_logs_query)
        cursor.execute(update_logs_query)
        conn.commit()

        return True
    except:
        return False


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
    print(data)
    things = []

    if data != None:
        for row in data:

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
            "action":row[2].encode('ascii'),
            "move":row[3],
            "remaining":row[4],
            "item":row[5].encode('ascii'),
            "location":row[6].encode('ascii')})

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

# ------------------All the various form tabs----------------------
# ------------------Add User Form ----------------------
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

# ------------------Add Item Form ----------------------
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

				itemname = form2.itemname.data

				reorderpt = form2.reorderpt.data
				batchqty = form2.batchqty.data
				category = form2.category.data
				unit = form2.unit.data
				price = form2.price.data
				categorystr = category.encode('ascii','ignore')

				if 'photo' in request.files:

					filename =photos.save(request.files['photo'])

				item = [itemname, reorderpt, batchqty, category, filename, unit,price]

				try:
					# TODO: string parameterisation
					conn = mysql.connect()
					cursor = conn.cursor()

					query = "INSERT INTO Items (name, reorder_pt, batch_qty, category, picture, unit, price) VALUES ('{}','{}','{}','{}','{}','{}','{}'); COMMIT".format(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
					cursor.execute(query)

					flash("Item has been added!", "success")
				except:
					flash("Oops! Something went wrong :(", "danger")

				return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Add Location form ----------------------

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

# ------------------Add Existing Items to New Locations form ----------------------

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
				amt = form4.qtyleft.data
				location=form4.location.data
				try:

					conn = mysql.connect()
					cursor = conn.cursor()
					cursor.execute("SELECT iid FROM Ascott_InvMgmt.Items WHERE name = '{}';".format(itemname))
					info = cursor.fetchone()

					# TODO: string parameterisation
					query = "INSERT INTO Ascott_InvMgmt.TagItems VALUES ('{}','{}','{}'); COMMIT".format(info,location,amt)
					# query = "INSERT INTO User VALUES ('{}','{}','{}','{}'); COMMIT".format(newuser[0],newuser[1],newuser[2],newuser[3])

					cursor.execute(query)
					flash("Added Item to Location %s!" %location, "success")
				except:
					flash("Oops! Something went wrong :(", "danger")

				return redirect(url_for('admin', lang_code=get_locale()))


@application.route('/<lang_code>/dashboard')
def dashboard():

    # user authentication
    logged_in = auth()
    if not logged_in:
        return redirect(url_for("login", lang_code=get_locale()))

    i = getInventoryLow()
    l = getDailyLogs()
    print(l)
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
    cats = cursor.fetchall()
    itemsByCat = []
    for cat in cats:
        itemsByCat.append({cat[0].encode('ascii'):[]})

    data = inventoryQuick(None)

    for i in data:
        print(type(i))
        for cat in itemsByCat:
            if cat.keys()[0] == i['category']:
                cat[i['category']].append(i)
                print(i['category'])

    print(itemsByCat)

    print(itemsByCat[0].keys()[0])

    print(itemsByCat[0])

    # A list of a dictionary of a list of dictionaries.

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
        categories = itemsByCat,
        num_cat = len(itemsByCat),
        shelves = shelves)

@application.route('/<lang_code>/inventory/<int:iid>', methods=['GET', 'POST'])
def item(iid):

    # user authentication
    if not session["logged_in"]:
        return redirect(url_for("login", lang_code=session["lang_code"]))

    if request.method == 'POST':
        print("form received")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = session['username']

        # form data
        location = request.form['location']
        qty = int(request.form['qty'])
        action = request.form['action']

        updateSuccess = stockUpdate(iid, location, qty, user, action, now)
        if updateSuccess:
            flash('Stock updated!', 'success')
        else:
            flash('Oops! Something went wrong :(', 'danger')


    cursor = mysql.connect().cursor()
    query = "SELECT name, category, picture, location, qty_left, reorder_pt, batch_qty, unit, price FROM Ascott_InvMgmt.view_item_locations WHERE iid = {};".format(iid)
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


    print(type(r[0]))

    # cursor.execute("SELECT new_price, date_effective FROM Ascott_InvMgmt.pricechange WHERE item = '{}';".format(iid))
    # price = cursor.fetchall()
    pricechanges = []
    # if price == ():
    #     pricechanges.append({
    #         "new_price": 0,
    #         "date_effective": 0})
    # else:

    #     for item in price:
    #         pricechanges.append({
    #             "new_price": item[0],
    #             "date_effective": item[1]})

    try:
        return render_template('item.html', item = r, pricechanges = pricechanges)
    except:
        return render_template('item.html', item = r, pricechanges = None)


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

    items = inventoryQuick(tag_id)

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
            updateSuccess = True
            for item, info in form_data.iterlists():
                iid = item
                inputQty = info[0]
                action = info[1]

                updateSuccess = stockUpdate(iid, tag_id, inputQty, user, action, now)

            flash('Success!', 'success')
        except:
            flash('Oops! Something went wrong :(', 'danger')

    return render_template('storeroom.html', things=items,
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
