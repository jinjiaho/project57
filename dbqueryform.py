from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

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

#----------get all required choices from database----------
def myDetails(required):
	location = []
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT %s FROM Ascott_InvMgmt.Items;" %(required))
	data1 = cursor.fetchall()
 	data2 = sorted(set(list(data1))) 
 	for i in data2:
 		y=str(i[0])
 		x=(y,y)
 		location.append(x)
 	return location

def myLocation(required):
	location = []
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT %s FROM Ascott_InvMgmt.LocationInfo;" %(required))
	data1 = cursor.fetchall()
 	data2 = sorted(set(list(data1))) 
 	for i in data2:
 		y=str(i[0])
 		x=(y,y)
 		location.append(x)
 	

 	return location





