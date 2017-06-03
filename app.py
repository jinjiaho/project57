from flask import Flask, render_template, request, session, redirect, url_for, flash
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
import os
import copy
from forms import LoginForm, RetrievalForm
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
#methods gives me all the items based on category
def getAllInventory(category):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT item, qtyLeft, picture FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))
    data = cursor.fetchall()
    items = []
    for item in data:
    	items.append(
    		{"name": item[0],
			"qty": item[1],
			"file": item[2]})
    
    return items

#methods gives me all the items based on NFC id.
def getFromLevels(idNFC):
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT item, category, idNFC FROM Ascott_InvMgmt.Items WHERE idNFC = '{}';".format(idNFC))

	data=cursor.fetchall()
	things = []
	for item in data:
		things.append(
			{"name": item[0],
			"category": item[1],
			"idNFC":item[2]})
	return things
		

#----------------------------ROUTING ------------------------

@app.route('/', methods=["GET", "POST"])
def login():
	
	error = ""
#create a login form to collect username, pass & role
	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else: 
			username = form.username.data
			password = form.password.data
			role = form.role.data
		
			cursor=mysql.connect().cursor()
			cursor.execute("SELECT username, password, role FROM User WHERE username= '" + username + "';")


			#check if user and pass data is correct by executing the db
			#data is stored as a tuple
			data = cursor.fetchone()
	
			if data is None: 
				# return redirect(url_for('login'))    #('Username does not exist.')
				# error = 'User does not exist'
				flash('User does not exist')
				return redirect(url_for('login'))

			elif password != data[1]:
				flash('Username and Password do not match.')
				return redirect(url_for('login'))

			elif role != data[2]:
				flash('Wrong position!')
				return redirect(url_for('login'))
			
			else:	
				if data[2] == "supervisor":
					session['logged_in'] = True
					session['username'] = username
					role = "supervisor"
					return redirect(url_for('hello'))
				elif data[2] =="attendant":
					session['logged_in'] = True
					session['username'] = username
					role = "ra"
					return redirect(url_for('scanner'))
				else:
					flash('Role is incorrect')
					return render_template('login.html', error=error)

	elif request.method =="GET":
		return render_template('login.html', form=form)



@app.route('/dashboard')
def hello():

    return render_template('dashboard.html')


@app.route('/inventory/')
def inventory():

    # get current list of all items listed in db
    supplies = getAllInventory('supplies')
    hampers = getAllInventory('hampers')
    kitchenware = getAllInventory('kitchenware')

    return render_template('inventory.html',
        all_guest_supplies = supplies,
        all_guest_hampers = hampers,
        all_kitchenware = kitchenware)

@app.route('/inventory/<item>')
def item(item):
	item = item
	return render_template('item.html', item=item)

@app.route('/logs')
def logs():
	return render_template('logs.html')

@app.route('/scanner')
def scanner():
	return render_template('scanner.html')

# RA shelf view
@app.route('/shelves/<tag_id>/', methods=['GET', 'POST'])
# @cache.cached(timeout=50)
def shelf(tag_id):
	if not session['logged_in']:
		return redirect(url_for('login'))
	if request.method == 'GET':
		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.execute("SELECT name, category, picture FROM Ascott_InvMgmt.Items WHERE idNFC = '{}';".format(tag_id))

		data=cursor.fetchall()
		things = []
		for item in data:
			things.append(
				{"name": item[0],
				"category": item[1],
				"picture":item[2]})
		return render_template('storeroom.html', role=role, things=things, cart_qty = len(cart))
	else: 
		item = request.form['item']
		qty = request.form['qty']
		updated = False
		for item in cart:
			if item['name']==item:
				item['qty'] = item['qty'] + qty
			updated = True
		if updated == False:
			cart.append({'name':item, 'qty': qty})
		return render_template('storeroom.html', role=role, cart_qty = len(cart))


@app.route('/shelves/<tag_id>/cart', methods=['GET', 'POST'])
def checkout(tag_id):
	if request.method == 'GET':
		return render_template('cart.html', role=role, cart=cart)
	else:
		now = datetime.now()
		form = request.form
		items = d.getlist['item']
		qtys = d.getlist['qty']
		user = session['username']

		conn = mysql.connect()
		cursor = conn.cursor()
		for i in range(0, len(items)):
			cursor.execute("SELECT name FROM Items WHERE name={} AND idNFC={};".format(items[i], tag_id))
			item = cursor.fetchone()[0]
			cursor.execute("INSERT INTO Logs (user, dateTime, action, qty, item, idNFC) VALUES ({}, {}, 'retrieval', {}, {}, {});".format(user, now, qtys[i], tag_id))
		cache = []
		flash("Success!")
		return redirect('scanner.html')

@app.route('/storeroom/')
def storeroom():
#get data input from idNFC from mobilephone. data output from db is in tuple
#this userinput is hard coded
	catItems = getFromLevels("Level4C2")
	return render_template("storeroom.html", catGoods=catItems)

@app.route('/storeroom/<things>', methods=["GET","POST"])	
def retrieval(things):
	things=things
	form = RetrievalForm()


	if request.method == "POST":
		if form.validate() == False:
			return render_template("retrieval.html",things=things,form=form)
		elif type(form.amount.data)!=int:
			return render_template("retrieval.html",things=things,form=form)

		else:	
			input = form.amount.data
			
			# flash('this has been added to the cart')
			# return redirect(url_for('storeroom/'))
			return ('you did it!!!!!')


	elif request.method=="GET":
		return render_template('retrieval.html',things=things, form=form)

	return render_template("retrieval.html", things=things)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	session.clear()
	role = ""

@app.route('/tasks')
def tasks():
	return render_template('tasks.html')

@app.route('/template')
def template():
	return render_template('template.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


## testing
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')