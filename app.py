from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=["GET", "POST"])
def login():
	error = ""
	if request.method == "POST":
		username = request.form['user']
		password = request.form['password']
		if username == "supervisor":
			if password == "supervisor":
				return redirect(url_for('hello'))
			else:
				error = "Password does not match username!"
		if username == "attendant":
			if password == "room":
				return redirect(url_for('scanner'))
			else:
				error = "Password does not match username!"
		else:
			error = "No such user!"
	return render_template('login.html', error=error)

@app.route('/dashboard')
def hello():
    return render_template('dashboard.html')

@app.route('/inventory/')
def inventory():
	return render_template('inventory.html')

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

@app.route('/storeroom')
def storeroom():
	return render_template('storeroom.html')

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