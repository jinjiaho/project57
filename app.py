from flask import Flask, render_template, request, session, redirect, url_for, flash
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import os
import copy
from forms import LoginForm, RetrievalForm

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


#----------------------------METHODS-------------------------
#methods gives me all the items based on category and amount in or out within the last month for each item
def getAllInventory(category):
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute(
		"SELECT idItem, item, qtyLeft, unit, picture, value FROM Ascott_InvMgmt.Items WHERE category = '{}';".format(category))

	data = cursor.fetchall()
	print(data)
	items = []
	for item in data:
		cursor.execute(
			"SELECT qty,action FROM ascott_invmgmt.logs WHERE dateTime between date_sub(NOW(), INTERVAL 1 month) AND NOW() AND idItem='{}';".format(item[0]))
		in_out_data = cursor.fetchall()
		delivered_out = 0
		recieved = 0
		for i in in_out_data:
			if i[1].encode('ascii') == 'out':
				delivered_out = delivered_out + int(i[0].encode('ascii'))
			else:
				recieved = recieved + int(i[0].encode('ascii'))
		remaining_quantity = item[2]
		initial_quantity = remaining_quantity + delivered_out - recieved
		items.append(
			{"name": item[1],
			"remaining": item[2],
			"unit": item[3],
			"starting": initial_quantity,
			"recieved": recieved,
			"demand": delivered_out,
			"file": item[4],
			"value": item[5]})
	
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


#methods gives me all the logs that occurred within the last 24 hours.
def getAllLogs():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(
		"SELECT uid, dateTime, action, qty, idItem,idNFC FROM Ascott_InvMgmt.Logs WHERE month(dateTime) = month(now()) AND year(dateTime) = year(now());")

	data=cursor.fetchall()
	things = []
	
	for row in data:
		cursor.execute(
			"SELECT name FROM Ascott_InvMgmt.User WHERE uid = '{}';".format(row[0]))
		user_data=cursor.fetchall()
		

		cursor.execute(
			"SELECT item, category FROM Ascott_InvMgmt.Items WHERE idItem = '{}';".format(row[4]))
		item_data=cursor.fetchall()

		things.append(
			{"name": user_data[0][0].encode('ascii'),
			"dateTime": row[1],
			"action":row[2],
			"qty":row[3],
			"item":item_data[0][0].encode('ascii'),
			"category":item_data[0][1].encode('ascii'),
			"location":row[5]})

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
		
			# cursor = mysql.connect().cursor()
			# sql = "SELECT username, password, role FROM Ascott_InvMgmt.User WHERE username="'+username+'";"
			# cursor.execute(sql)
			# db = MySQLdb.connect(host="localhost", port = 3306, user = "root", password="classroom",db="Ascott_InvMgmt")
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
					return redirect(url_for('hello'))
				elif data[2] =="attendant":
					session['logged_in'] = True
					session['username'] = username
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
		supplies = supplies,
		hampers = hampers,
		kitchenware = kitchenware)

@app.route('/inventory/<category>/<item>')
def item(item, category):
	item = item
	category = category
	return render_template('item.html', item=item, category=category)

@app.route('/inventory/<category>')
def category(category):
	category = category
	itemtype = getAllInventory(category)
	return render_template('category.html', category=category, itemtype=itemtype)

@app.route('/logs')
def logs():
	logs=getAllLogs()
	return render_template('logs.html',logs=logs)

@app.route('/scanner')
def scanner():
	return render_template('scanner.html')

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


	
	return render_template("retrieval.html",things=things)

@app.route('/tasks')
def tasks():
	return render_template('tasks.html')
	
@app.route('/user', methods=["GET"])
def user():
	return render_template('user.html')

@app.route('/icons')
def icons():
	return render_template('icons.html')

@app.route('/maps')
def maps():
	return render_template('maps.html')

@app.route('/notifications')
def notifications():
	return render_template('notifications.html')

@app.route('/table')
def table():
	return render_template('table.html')

@app.route('/template')
def template():
	return render_template('template.html')

@app.route('/typography')
def typography():
	return render_template('typography.html')

@app.route('/upgrade.html')
def upgrade():
	return render_template('upgrade.html')

@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, nothing at this URL.', 404



## testing
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')