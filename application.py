from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, g, json
from flask_babel import Babel
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from forms import LoginForm, RetrievalForm, AddUserForm, CreateNewItem,AddNewLocation,ExistingItemsLocation, RemoveItem, TransferItem
from apscheduler.schedulers.background import BackgroundScheduler
# from exceptions import InsufficientQtyError, ContainsItemsError
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import os, copy, re, csv, json_decode, imaging, pytz
# from flask.ext.cache import Cache


# pip2 install flask
# pip2 install mysql-python
# pip2 install mysqlclient
# pip2 install flask-SQLAlchemy
# pip2 install flask-babel
# pip2 install flask-wtf
# pip2 install flask-mysql
# pip2 install flask-uploads
# pip2 install pytz
# pip2 install numpy
# pip2 install scipy
# pip2 install statsmodels
# pip2 install pandas
# pip2 install Pillow
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
application.config.from_pyfile('amazonRDS.py') # override with instanced configuration (in "/instance"), if any
#application.config.from_pyfile('myConfig1.py')
#application.config.from_pyfile('myConfig2.py')

# Babel init
babel = Babel(application)

# mysql init
mysql = MySQL()
mysql.init_app(application)

# global vars
adminmode = False
role = ""

# Configure the image uploading via Flask-Uploads
photos = UploadSet('images', IMAGES)
configure_uploads(application, photos)
sched = BackgroundScheduler()

# jobstores = {
#     'mongo': MongoDBJobStore(),
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }

# Exception classes, feel free to use.
# Called in admin()
class InsufficientQtyError(Exception):
    pass

class ContainsItemsError(Exception):
    pass
class InvalidPasswordError(Exception):
    pass

###########################
##        METHODS        ##
###########################

# TODO: encapsulate all methods in separate classes and .py files

# Query for form select fields.
# Currently called by admin()
def choices(table, column, *args):
    choices = []
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT {} FROM {}".format(column, table)
    cursor.execute(query)
    data1 = cursor.fetchall()
    data2 = sorted(set(list(data1)))
    for i in data2:
        y=str(i[0])
        x=(y,y)
        choices.append(x)
    return choices

# For populating select fields in admin forms with tags.
# Called by admin()
def storeTags():
    choices = []
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT tid, tname, storeroom FROM TagInfo;")
    data = sorted(set(list(cursor.fetchall())))
    for d in data:
        value = d[0]
        text = str(d[2]) + " - " + str(d[1])
        pair = (value, text)
        choices.append(pair)
    return choices

def getAllTags():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT tid, tname, storeroom, remarks FROM TagInfo;")
    data = sorted(set(list(cursor.fetchall())))
    allTags = []
    for i in data:
        allTags.append({
            'tid': i[0],
            'tname': i[1].encode('ascii'),
            'storeroom': i[2].encode('ascii'),
            'remarks': i[3].encode('ascii')
            })
    return allTags

# Returns all the items based on category and amount in or out within the last month for each item
# Called by category()
def getAllInventory(category):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT iid, name, qty_left, reorder_pt, out_by, picture, category, ROUND(price,2) FROM Ascott_InvMgmt.view_item_locations WHERE category = '{}';".format(category))
    data = cursor.fetchall()
    print(data)

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
            "SELECT action, qty_moved FROM Ascott_InvMgmt.Logs WHERE month(date_time) = month(now()) AND year(date_time) = year(now()) AND item={};".format(item[0]))
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
            "SELECT qty_left FROM Ascott_InvMgmt.view_item_locations WHERE iid={};".format(item[0]))
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
    conn = mysql.connect()
    cursor = conn.cursor()
    if location == None:
        cursor.execute("""SELECT iid, name, category, picture, SUM(qty_left), reorder_pt, out_by FROM view_item_locations
                        GROUP BY iid;""")
        data = cursor.fetchall()
        for d in data:
            items.append(
                {"iid":d[0],
                "name": d[1].encode('ascii'),
                "category": d[2].encode('ascii'),
                "picture": d[3].encode('ascii'),
                "remaining": d[4],
                "reorder": d[5],
                "unit": d[6].encode('ascii')
                })
    else:
        cursor.execute("""SELECT iid, name, category, picture, out_by FROM view_item_locations
                        WHERE tag='{}' AND reorder_pt >= 0;""".format(location))
        data = cursor.fetchall()
        conn.commit()
        for d in data:
            items.append(
                {"iid":d[0],
                "name": d[1].encode('ascii'),
                "category": d[2].encode('ascii'),
                "picture":d[3].encode('ascii'),
                "unit":d[4].encode('ascii')
                })
    return items

# Stock Update Function for RA, Runner and Supervisors.
# Called by item() and shelf().
# Returns True if the stock was updated successfully, False otherwise.
def stockUpdate(iid, tagId, inputQty, user, action, time):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT qty_left, in_out_ratio FROM view_item_locations WHERE iid='{}' AND tag='{}';".format(iid, tagId))
        data = cursor.fetchall()
        old_qty = data[0][0]

        if action == 'out':
            qty_left = old_qty  - inputQty
            qty_diff = inputQty * (-1)     # make qty_input negative to reflect taking qty OUT of store.

            if qty_left < 0:
                raise InsufficientQtyError("Not enough in store!")

        elif action == 'in':
            print inputQty
            print(inputQty*data[0][1])
            qty_left = old_qty + inputQty*data[0][1]
            qty_diff = qty_left - old_qty
        else:
            qty_left = inputQty
            qty_diff = qty_left - old_qty # change the value of qty to the difference
        conn = mysql.connect()
        cursor = conn.cursor()
        update_items_query = "UPDATE TagItems SET qty_left={} WHERE iid={} AND tag={};".format(qty_left, iid, tagId)

        # general query for all actions
        # print(update_items_query)
        cursor.execute(update_items_query)
        conn.commit()

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT storeroom FROM TagInfo WHERE tid={};".format(tagId))
        location = cursor.fetchall()[0][0]
        # Log action
        # conn = mysql.connect()
        # cursor = conn.cursor()
        update_logs_query = """INSERT INTO Logs (user, date_time, action, qty_moved, qty_left, item, location)
                                VALUES ('{}', '{}', '{}', {}, {}, {}, '{}');""".format(user, time, action, qty_diff, qty_left, iid, location)
        # print(update_logs_query)
        cursor.execute(update_logs_query)
        conn.commit()

        return ['Success!', "success"]

    except InsufficientQtyError as e:
        return [e.args[0], "danger"]

    except Exception as e:
        return ["STOCK UPDATE ERROR: %s" % e, "danger"]


# Returns all the items based on location. KIV for possible supervisor view filtering.
def getFromLevels(location):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name, category, tag FROM Ascott_InvMgmt.view_item_locations WHERE tag={};".format(location))

    data=cursor.fetchall()
    things = []
    for item in data:
        things.append(
            {"name": item[0],
            "category": item[1],
            "location":item[2]})
    return things



# Returns the logs that occurred within the current month.
# Called by logs()
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
            print(row[5])
            cursor.execute("SELECT name, category FROM Items WHERE iid={};".format(row[5]))
            info = cursor.fetchall()[0]
            item_name = info[0].encode('ascii')
            category = info[1].encode('ascii')

            things.append({"name": row[0].encode('ascii'),
                "dateTime": row[1],
                "action":row[2],
                "move":row[3],
                "remaining":row[4],
                "category":category,
                "item":item_name,
                "location":row[6]})
            # print(things)

    return things


# Returns inventory items that are below threshold levels
# Called by dashboard()
def getInventoryLow():

    THRESHOLD = 1.2
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT iid, name, qty_left, reorder_pt, picture, category, out_by FROM Ascott_InvMgmt.view_item_locations
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
            "category": i[5].encode('ascii'),
            "unit":i[6].encode('ascii')})

    return r

# Called by dashboard()
def getDailyLogs():

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user, date_time, action, qty_moved, qty_left, item, location FROM Ascott_InvMgmt.Logs WHERE day(date_time) = day(now());")
    conn.commit()
    data=cursor.fetchall()
    things = []


    for row in data:
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT name FROM Items WHERE iid={};".format(row[5]))
        item_name = cursor.fetchall()[0][0]

        things.append({"name": row[0].encode('ascii'),
            "dateTime": row[1],
            "action":row[2].encode('ascii'),
            "move":row[3],
            "remaining":row[4],
            "item":item_name.encode('ascii'),
            "location":row[6].encode('ascii')})
    return things


# POST for getting chart data
@application.route('/api/getChartData', methods=["POST"])
def getChartData():

    print "CHART: content_type - ", request.content_type
    print "CHART: request.json - ", request.json

    if not request.json:
        print "CHART: Bad JSON format, aborting chart creation..."
        page_not_found(400)
    else:
        items = request.get_json()
        iid = items[0]["iid"]
        r = []

        conn = mysql.connect()
        cursor = conn.cursor()

        for i in items:
            # get transaction logs per tag
            tag = i["tag"]
            query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = {} AND location = '{}'".format(iid, tag)
            cursor.execute(query)
            data = cursor.fetchall()
            r.append({
                "loc": i["location"],
                "val": data})

        return jsonify(r)

# POST for getting chart data
@application.route('/api/editReorder', methods=["POST"])
def editReorder():

    print "REORDER: content_type - ", request.content_type
    print "REORDER: request.json - ", request.json

    if not request.json:
        print "REORDER: Bad JSON format, aborting reorder modification..."
        page_not_found(400)
    else:
        data = request.get_json()
        name = data["name"].encode('ascii')
        reorder = data["reorder"]

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Ascott_InvMgmt.Items SET reorder_pt={} WHERE (name='{}' AND iid > 0);".format(reorder, name))
        conn.commit()

        return jsonify("")

@application.route('/api/editPrice', methods=["POST"])
def editPrice():

    print "PRICECHANGE: content_type - ", request.content_type
    print "PRICECHANGE: request.json - ", request.json

    if not request.json:
        print "PRICECHANGE: Bad json format, aborting reorder modification..."
        page_not_found(400)

    else:
        data = request.get_json()
        iid = data["iid"].encode('ascii')
        newprice = data["newprice"].encode('ascii')
        effectdate = data["effectdate"].encode('ascii')
        effectdate1 = datetime.strptime(effectdate , '%Y-%m-%d')
        # print(type(effectdate1))

        # conn = mysql.connect()
        # cursor = conn.cursor()
        # cursor.execute(
        #   "SELECT COUNT(*) FROM Ascott_InvMgmt.PriceChange WHERE item = '{}'".format(iid))
        # price_changed=cursor.fetchall()

        # conn = mysql.connect()
        # cursor = conn.cursor()
        # if price_changed[0][0] == 1:

        #   cursor.execute(
        #       "UPDATE Ascott_InvMgmt.PriceChange SET new_price= '{}' , date_effective= STR_TO_DATE( '{} 00:00:00', '%Y-%m-%d %H:%i:%s') WHERE (item = '{}');".format(newprice, effectdate, iid))
        #   conn.commit()

        # elif price_changed[0][0] == 0:

        #   cursor.execute(
        #       "INSERT INTO Ascott_InvMgmt.PriceChange (item, new_price, date_effective) VALUES ('{}' ,'{}' ,'{}');".format(iid, newprice, effectdate))
        #   conn.commit()

        try:
            sched.remove_job(iid, jobstore=None)
        except:
            pass
        # The job will be executed on effectdate
        sched.add_job(priceChangenow, 'date', run_date=effectdate1, args=[iid,newprice], id=iid)
        sched.print_jobs(jobstore=None)

        # sched.start()
        # print(sched.jobstores)

        # idItem = cursor.fetchone()

        # # query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = {0}".format(idItem)
        # query = "SELECT date_time, qty_left FROM Ascott_InvMgmt.Logs WHERE item = 1"
        # # TODO: string parameterisation
        # # query = "SELECT datetime, qtyAfter FROM Ascott_InvMgmt.Logs WHERE idItem = {}".format(idItem)
        # cursor.execute(query)
        # responseData = cursor.fetchall()

        return jsonify("")

def priceChangenow(iid,price):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE Ascott_InvMgmt.Items SET price='{}' WHERE (iid = '{}');".format(iid,price))
        conn.commit()

        # conn = mysql.connect()
        # cursor=conn.cursor()
        # cursor.execute("DELETE FROM Ascott_InvMgmt.PriceChange WHERE (item = '{}');".format(iid))
        # conn.commit()


        return



# true if user is authenticated, else false
# used in ALL ROUTES
def auth():
    if u'logged_in' in session:
        return session['logged_in']
    return False

# wrapper function for route redirection
def filter_role(roles_routes):
    for k,v in roles.items():
        if session['role'] == k:
            return redirect(v)


# used as a Jinja template in HTML files
@application.template_filter('lang_strip')
def lang_strip(s):
    l = re.search(r"(?m)(?<=(en\/)|(zh\/)|(ms\/)|(ta\/)).*$", str(s.encode('ascii')))
    if l:
        return l.group()
    return None

# used as a Jinja template in HTML files
@application.template_filter('curr_time')
def curr_time(s):
    tz = pytz.timezone(application.config["TIMEZONE"])
    return s+datetime.now(tz).strftime('%I:%M %p')

# used as a Jinja template in HTML files
@application.template_filter('prop_name')
def prop_name(s):
    return s+application.config["PROP_NAME"]

# case query for mobile input
def input_handler(qty, user):
    query = 'UPDATE TagItems SET qty_left = CASE WHERE iid={} WHEN action'
    # Issue: Need iid argument.

# fires right before each request is delivered to the relevant route
@application.before_request
def before():
    # localization setting
    if request.view_args and 'lang_code' in request.view_args:
        if request.view_args['lang_code'] not in application.config["BABEL_LOCALES"]:
            g.current_lang = application.config["BABEL_DEFAULT_LOCALE"]
        else:
            g.current_lang = request.view_args['lang_code']
            session["lang_code"] = g.current_lang
            request.view_args.pop('lang_code')
    else:
        session["lang_code"] = application.config["BABEL_DEFAULT_LOCALE"]
        g.current_lang = session["lang_code"]

    # user authentication
    if u'logged_in' not in session:
        session["logged_in"] = False

@application.after_request
def add_header(r):
    r.headers['Cache-Control'] = 'public, max-age=0'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    return r

# used in setting locale for each route
# used in ALL ROUTES
@babel.localeselector
def get_locale():
    return g.get('current_lang', 'en')

@application.after_request
def add_header(response):
    response.cache_control.max_age=0
    return response

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
        elif session['role'] == "runner":
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
            cursor.execute("SELECT username, password, role, name FROM User WHERE username= '{}';".format(username))

            # check if user and pass data is correct by executing the db
            # data is stored as a tuple
            data = cursor.fetchone()

            if data is None:
                # username does not match records
                flash('User does not exist')
                return redirect(url_for("login", lang_code=get_locale()))

            # elif password != hashpass:
            elif check_password_hash(data[1], password) == False:
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
                if session['role'] == "supervisor":
                    if "next" in session:
                        return redirect(session.pop('next'))
                    else:
                        return redirect(url_for("dashboard", lang_code=get_locale()))
                elif session['role'] == "attendant" or session['role'] == "runner":
                    if "next" in session:
                        return redirect(session.pop('next'))
                    else:
                        return redirect(url_for("scanner", lang_code=get_locale()))

    elif request.method == "GET":

        # user authentication
        if not auth():
            return render_template("login.html", form=form)
        else:
            # user already logged_in previously
            if session['role'] == "supervisor":
                return redirect(url_for("dashboard", lang_code=get_locale()))
            elif session['role'] == "attendant":
                return redirect(url_for("scanner", lang_code=get_locale()))
            elif session['role'] == "runner":
                return redirect(url_for("scanner", lang_code=get_locale()))


@application.route('/<lang_code>/admin', methods=["GET","POST"])
def admin():

    form = AddUserForm()
    form2 = CreateNewItem()
    form3 = AddNewLocation()
    form4 = ExistingItemsLocation()
    removeItemForm = RemoveItem()
    transferItemForm = TransferItem()


    storeTagChoices = storeTags()
    allTags = getAllTags()
    print allTags
    roles = choices('Permissions', 'role')
    categories = ['Guest Hamper', 'Guest Supplies', 'Kitchenware']

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT name, tag FROM view_item_locations;")
    itemTags = cursor.fetchall()

    # Initialize options for all select fields
    form.role.choices = roles
    form2.category.choices = choices('Items', 'category')
    form3.location.choices = choices('TagInfo', 'storeroom')
    form4.tid.choices = storeTagChoices
    removeItemForm.iname.choices = choices('Items', 'name')
    transferItemForm.tagOld.choices = storeTagChoices
    transferItemForm.tagNew.choices = storeTagChoices


    #--------------users table-------------------------
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT role, name, username FROM Ascott_InvMgmt.User;")

    data = cursor.fetchall()
    # print(data)
    things = []
    for item in data:
        things.append(
            {"role": item[0],
            "name": item[1],
            "username": item[2]})

#-------------NFCID----------------------------------

    cursor.execute("SELECT DISTINCT tag FROM Ascott_InvMgmt.TagItems;")

    data1 = cursor.fetchall() #displays all unique NFC id tags.

    NFCs=[]
    group={}
    items=[]

    for idNFC in data1:
        NFCs.append(idNFC[0])

    for i in NFCs:
        try:
            #fetch all item names pertaining to the tag.
            cursor.execute("SELECT name, iid, qty_left FROM Ascott_InvMgmt.view_item_locations WHERE tag = {};".format(i))
            data3=cursor.fetchall()

            cursor.execute("SELECT tname FROM TagInfo WHERE tid={};".format(i))
            l_name = cursor.fetchall()[0][0]

            group[(i, l_name)] = data3
        except:
            pass

    if request.method =="GET":

        # user authentication
        if not auth():
            session['next'] = request.url
            return redirect(url_for("login", lang_code=get_locale()))

        cursor.execute("SELECT DISTINCT name FROM Ascott_InvMgmt.Items;")
        items = cursor.fetchall()
        # print (items)
        flat_items = [item.encode('ascii') for sublist in items for item in sublist]
        return render_template('admin.html',
            form=form,
            form2=form2,
            form3=form3,
            form4=form4,
            removeItemForm=removeItemForm,
            transferItemForm = transferItemForm,
            tagsByStore = json.dumps(storeTagChoices),
            itemTags = json.dumps(itemTags),
            cat_list = categories,
            users=things,
            tags = allTags,
            group=group,
            item_list=flat_items)

# ------------------All the various form tabs----------------------

# ------------------Add User Form ----------------------
    elif request.method == "POST":

        if request.form['name-form'] =='form':
            if form.validate() == False:
                flash("Failed to validate form", "danger")
                return render_template('admin.html',
                    form=form,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    removeItemForm=removeItemForm,
                    transferItemForm = transferItemForm,
                    tagsByStore = json.dumps(storeTagChoices),
                    itemTags = json.dumps(itemTags),
                    cat_list = categories,
                    users=things,
                    tags = allTags,
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
                query = "INSERT INTO User VALUES ('{}','{}','{}','{}');".format(newuser[0],newuser[1],newuser[2],newuser[3])
                # query = "INSERT INTO User (username,password,role,name) VALUES ();"
                # print(query)
                cursor.execute(query)
                conn.commit()
                # cursor.execute("COMMIT")
                flash("User has been added!", "success")
                return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Edit User Form ----------------------
        elif request.form['name-form'] =='editUserForm':

            try:
                username = request.form["username"]
                role = request.form["role"]
                name = request.form["name"]
                password = request.form["password"]
                query = ""
                messages = []

                if role:
                    query += "UPDATE User SET role='{}' WHERE username='{}';".format(role, username)
                    messages.append(["User role updated to "+role, "success"])
                if name:
                    query += "UPDATE User SET name='{}' WHERE username='{}';".format(name, username)
                    messages.append(["Name updated to "+name, "success"])
                if password:
                    if auth():
                        query += "UPDATE User SET password='{}' WHERE username='{}';".format(generate_password_hash(password), username)
                        messages.append(["Password updated!", "success"])
                    else:
                        raise Exception("User authentication failed, please login again.")
                conn = mysql.connect()
                cursor = conn.cursor()
                print query
                cursor.execute(query)
                conn.commit()
                for i in messages:
                    flash(i[0], i[1])
            except:
                flash(e.args[0], "danger")

            return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Delete User Form ----------------------
        elif request.form['name-form'] =='deleteUser':
            print('form received')
            username = request.form["username"]

            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "DELETE FROM User WHERE username='{}';".format(username)
                print(query)
                cursor.execute(query)
                conn.commit()
                flash("User deleted!", "success")
            except:
                flash("Oops! Something went wrong :(", "danger")

            return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Add Item Form ----------------------
        elif request.form['name-form'] =='form2':
            if form2.validate() == False:
                flash("Failed to validate form", "danger")
                return render_template('admin.html',
                    form=form,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    removeItemForm=removeItemForm,
                    transferItemForm = transferItemForm,
                    tagsByStore = json.dumps(storeTagChoices),
                    itemTags = json.dumps(itemTags),
                    cat_list = categories,
                    users=things,
                    tags = allTags,
                    group=group)
            else:

                itemname = form2.itemname.data
                reorderpt = form2.reorderpt.data
                category = form2.category.data
                price = form2.price.data
                out_by = form2.count_unit.data
                in_by = form2.order_unit.data
                in_out_ratio = form2.order_multiplier.data


                if 'photo' in request.files:
                    try:
                        filename = photos.save(request.files['photo'])
                    except:
                        filename = "default.thumb"
                        flash('Photo selected is not a valid file', "danger")

                    thumbnail = imaging.Imaging().thumb(filename)

                item = [itemname, category, thumbnail, price, reorderpt, out_by, in_by, in_out_ratio]
                print(item)
                try:
                    # TODO: string parameterisation
                    conn = mysql.connect()
                    cursor = conn.cursor()

                    # TODO: Change form to input appropriate information
                    query = "INSERT INTO Items (name, category, picture, price, reorder_pt, out_by, in_by, in_out_ratio) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');".format(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7])
                    cursor.execute(query)
                    conn.commit()

                    flash("Item has been added! Next, please assign a tag.", "success")

                except Exception as e:
                    print(e)
                    flash("Oops! Something went wrong :(", "danger")

                return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Remove Item Form ----------------------
        elif request.form['name-form'] == 'removeItemForm':
            if removeItemForm.validate() == False:
                flash("Failed to validate form", "danger")
                return render_template('admin.html',
                    form=form,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    removeItemForm=removeItemForm,
                    transferItemForm = transferItemForm,
                    tagsByStore = json.dumps(storeTagChoices),
                    itemTags = json.dumps(itemTags),
                    cat_list = categories,
                    users=things,
                    tags = allTags,
                    group=group)

            else:
                iname = removeItemForm.iname.data

                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT iid, picture FROM Items WHERE name='{}';".format(iname))
                response = cursor.fetchall()[0]
                try:
                    iid, picture = response[0], response[1].encode("ascii")
                    print "ADMIN: Deleting item #%s with thumbnail '%s' ..." % (iid, picture)

                    removeFromItems = "DELETE FROM Items WHERE name='{}';".format(iname)
                    print "SQL: %s" % removeFromItems
                    cursor.execute(removeFromItems)
                    conn.commit()

                    removeFromTagItems = "DELETE FROM TagItems WHERE iid='{}';".format(iid)
                    print "SQL: %s" % removeFromTagItems
                    cursor.execute(removeFromTagItems)
                    conn.commit()

                    try:
                        os.remove("static/img/items/"+picture)
                        print("ADMIN: Item successfuly deleted!")
                    except Exception as e:
                            print("DELETE THUMBNAIL: %s" % e)

                    flash('Item deleted!', 'success')

                except IndexError:
                    flash("Item not found!", "warning")

                except Exception as e:
                    print("DELETE ITEM: %s" % e)
                    flash('Couldn\'t delete item', 'danger')

            return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Add Existing Items to New Locations form ----------------------

        elif request.form['name-form'] =='form4':
            if form4.validate() == False:
                flash("Failed to validate form", "danger")
                return render_template('admin.html',
                    form=form,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    removeItemForm=removeItemForm,
                    transferItemForm = transferItemForm,
                    tagsByStore = json.dumps(storeTagChoices),
                    itemTags = json.dumps(itemTags),
                    cat_list = categories,
                    users=things,
                    tags = allTags,
                    group=group)
            else:
                itemname = form4.itemname.data
                tid = form4.tid.data
                amt = form4.qty.data
                try:

                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute("SELECT iid FROM Ascott_InvMgmt.Items WHERE name = '{}';".format(itemname))
                    iid = cursor.fetchall()[0][0]

                    # TODO: string parameterisation

                    # cursor = mysql.connect().commit();
                    # Check if item is already assigned to tag
                    cursor.execute("SELECT * FROM Ascott_InvMgmt.TagItems WHERE iid={} AND tag={};".format(iid, tid))
                    rowExists = cursor.fetchall()

                    if rowExists:
                        cursor.execute("UPDATE TagItems SET qty_left={} WHERE iid={} AND tag={};".format(amt, iid, tid))
                        conn.commit()
                        flash("Item already in location. Qty updated.", "success")

                    else:
                        query = "INSERT INTO Ascott_InvMgmt.TagItems VALUES ({},{},{}); COMMIT;".format(iid,tid,amt)
                        print(query)
                        cursor.execute(query)
                        flash("Added Item to Location!", "success")

                except:
                    flash("Oops! Something went wrong :(", "danger")

                return redirect(url_for('admin', lang_code=get_locale()))


# ------------------ Transfer Items Form ----------------------

        elif request.form['name-form'] =='transferItemForm':
            if transferItemForm.validate() == False:
                flash("Failed to validate form", "danger")
                return render_template('admin.html',
                    form=form,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    removeItemForm=removeItemForm,
                    transferItemForm = transferItemForm,
                    tagsByStore = json.dumps(storeTagChoices),
                    itemTags = json.dumps(itemTags),
                    cat_list = categories,
                    users=things,
                    tags = allTags,
                    group=group)
            else:
                print("form validated")
                item = transferItemForm.iname.data
                tagOld = transferItemForm.tagOld.data
                tagNew = transferItemForm.tagNew.data
                qty = transferItemForm.qty.data
                print(item)
                print(tagOld)
                print(tagNew)
                print(qty)

                try:
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "SELECT iid FROM Ascott_InvMgmt.Items WHERE name = '{}';".format(item)
                    print(query)
                    cursor.execute(query)
                    iid = cursor.fetchall()[0][0]

                    query = "SELECT * FROM TagItems WHERE iid={} AND tag={};".format(iid, tagOld)
                    print(query)
                    cursor.execute(query)

                    row = cursor.fetchall()[0]

                    # TODO: string parameterisation
                    queryOut = ""
                    queryIn = ""
                    message = ""

                    # if user only wants to transfer some of the items over
                    if qty:
                        if qty == 0:
                            flash("Qty input was 0, none transferred.", "warning")
                            return redirect(url_for('admin', lang_code=get_locale()))
                        print(row)
                        # check if there are enough items at the old location to transfer the stated qty.
                        if qty > row[2]:
                            raise InsufficientQtyError("Not enough in store to transfer!")
                        # if sufficient items, deduct items from old location.
                        qty_left = row[2] - qty
                        if qty_left == 0:
                            queryOut = "DELETE FROM TagItems WHERE iid={} AND tag={};".format(iid, tagOld)
                        else:
                            queryOut = "UPDATE TagItems SET qty_left={} WHERE iid={} AND tag={};".format(qty_left, iid, tagOld)

                    # if user wants to transfer all
                    else:
                        qty = row[2]
                        queryOut = "DELETE FROM TagItems WHERE iid={} AND tag={};".format(iid, tagOld)

                    print(queryOut)

                    # Add the items to the new location.
                    # Check if there are already instances of the item at the new location.
                    query = "SELECT * FROM Ascott_InvMgmt.TagItems WHERE iid={} AND tag={};".format(iid, tagNew)
                    print(query)
                    cursor = mysql.connect().cursor()
                    cursor.execute(query)
                    rowExists = cursor.fetchall()

                    if rowExists:
                        print('row exists!')
                        # Update the qty instead of creating a new row.
                        newQty = rowExists[0][2] + qty
                        queryIn = "UPDATE TagItems SET qty_left={} WHERE iid={} AND tag={};".format(newQty, iid, tagNew)
                        message = "Item already in location, updated qty."

                    else:
                        print('row does not exist')
                        # Create a new row.
                        queryIn = "INSERT INTO Ascott_InvMgmt.TagItems VALUES ({},{},{});".format(iid, tagNew, qty)
                        message = "Transferred item to location!"
                    print(queryIn)
                    flash(message, "success")

                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(queryIn + queryOut + "COMMIT;")


                except InsufficientQtyError as e:
                    flash(e.args[0], "danger")
                except:
                    flash("Oops! Something went wrong :(", "danger")

                return redirect(url_for('admin', lang_code=get_locale()))

# ------------------Remove Item From Tag Form ----------------------
        elif request.form['name-form'] =='removeFromTag':
            print('form received')
            item = request.form["iid"]
            tag = request.form["tid"]

            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                query = "DELETE FROM TagItems WHERE iid={} AND tag={};".format(item, tag)
                print(query)
                cursor.execute(query)
                conn.commit()
                flash("Item removed from tag!", "success")
            except:
                flash("Oops! Something went wrong :(", "danger")

            return redirect(url_for('admin', lang_code=get_locale()))


# ------------------Add Tag form ----------------------
        # TODO: Change form to get appropriate values
        elif request.form['name-form'] =='form3':
            if form3.validate() == False:
                flash("Failed to validate form", "danger")
                return render_template('admin.html',
                    form=form,
                    form2=form2,
                    form3=form3,
                    form4=form4,
                    removeItemForm=removeItemForm,
                    transferItemForm = transferItemForm,
                    tagsByStore = json.dumps(storeTagChoices),
                    itemTags = json.dumps(itemTags),
                    cat_list = categories,
                    users=things,
                    tags = allTags,
                    group=group)
            else:
                tname = form3.tname.data
                oldLocation = form3.location.data
                newLocation = form3.newLocation.data
                remarks = form3.remarks.data

                if newLocation:
                    location = newLocation
                else:
                    location = oldLocation

                conn = mysql.connect()
                cursor = conn.cursor()
                try:
                    # TODO: string parameterisation
                    query = "INSERT INTO TagInfo (`tname`, `storeroom`, `remarks`) VALUES ('{}','{}','{}');".format(tname, location, remarks)
                    print(query)
                    cursor.execute(query)
                    conn.commit()
                    flash("New Tag Added!", "success")
                except:
                    flash("Couldn't add tag.", "danger")

                return redirect(url_for('admin', lang_code=get_locale()))


# ------------------Delete Tag form ----------------------
        elif request.form['name-form'] =='deleteTag':
            print('form received')
            tid = request.form["tid"]

            try:
                conn = mysql.connect().cursor()
                cursor.execute("SELECT * FROM TagItems WHERE tag={};".format(tid))
                tagRows = cursor.fetchone()
                if tagRows:
                    raise ContainsItemsError("Can't delete tag because it has items assigned to it. Please remove the items from the tag before deleting the tag.")
                else:
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    query = "DELETE FROM TagInfo WHERE tid={};".format(tid)
                    print(query)
                    cursor.execute(query)
                    conn.commit()
                    flash("Tag deleted!", "success")

            except ContainsItemsError as e:
                flash(e.args[0], "danger")
            except:
                flash("Oops! Something went wrong :(", "danger")

            return redirect(url_for('admin', lang_code=get_locale()))



@application.route('/<lang_code>/dashboard')
def dashboard():

    # user authentication
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))
    if session['role'] != "supervisor":
        return redirect(url_for("scanner", lang_code=get_locale()))

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
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))
    if session['role'] != "supervisor":
        return redirect(url_for("scanner", lang_code=get_locale()))

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT DISTINCT category FROM Items;")
    cats = cursor.fetchall()
    itemsByCat = []
    for cat in cats:
        itemsByCat.append({cat[0].encode('ascii'):[]})

    data = inventoryQuick(None)

    for i in data:
        for cat in itemsByCat:
            if cat.keys()[0] == i['category']:
                cat[i['category']].append(i)
                print(i['category'])


    # get list of all locations to display
    location_query = "SELECT DISTINCT TagInfo.storeroom FROM TagItems INNER JOIN TagInfo ON TagItems.tag = TagInfo.tid;"
    cursor = mysql.connect().cursor()
    cursor.execute(location_query)
    data = cursor.fetchall()
    locations = []

    for i in data:
        locations.append(i[0].encode('ascii'))

    return render_template('inventory.html',
        user = session['username'],
        role = session['role'],
        categories = itemsByCat,
        num_cat = len(itemsByCat),
        locations = locations)

@application.route('/<lang_code>/inventory/<int:iid>', methods=['GET', 'POST'])
def item(iid):

    # user authentication
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))
    if session['role'] != "supervisor":
        return redirect(url_for("scanner", lang_code=get_locale()))

    if request.method == 'POST':

        print "STOCK UPDATE: content_type - ", request.content_type

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = session['username']

        # form data
        tid = int(request.form.get('location'))
        qty = int(request.form.get('qty'))
        action = request.form.get('action')
        print("STOCK UPDATE: Form received - (iid: %s ,tid: %s, qty: %s , action: %s, user: %s)" %
            (iid, tid, qty, action, user))

        try:
            # process changes
            updateSuccess = stockUpdate(iid, tid, qty, user, action, now)
            flash(updateSuccess[0], updateSuccess[1])
            return redirect(url_for("item", lang_code=get_locale(), iid=iid))
        except:
            flash('Oops! Something went wrong :(', 'danger')
            return redirect(url_for("item", lang_code=get_locale(), iid=iid))

    cursor = mysql.connect().cursor()
    query = "SELECT name, category, picture, tag, qty_left, reorder_pt, in_out_ratio, out_by, price FROM Ascott_InvMgmt.view_item_locations WHERE iid = {};".format(iid)
    cursor.execute(query)
    data = cursor.fetchall()
    # d = [[s.encode('ascii') for s in list] for list in data]
    r = []
    for i in data:
        cursor.execute("SELECT tname, storeroom FROM TagInfo WHERE tid={};".format(i[3]))
        taginfo = cursor.fetchall()[0]
        tname = taginfo[0].encode('ascii')
        storeroom = taginfo[1].encode('ascii')

        r.append({"name": i[0].encode('ascii'),
            "category": i[1].encode('ascii'),
            "picture": i[2].encode('ascii'),
            "tag": tname,
            "location": storeroom,
            "qty_left": i[4],
            "reorder": i[5],
            "batch_size": i[6],
            "unit": i[7].encode('ascii'),
            "price": round(i[8],2),
            "tid": i[3],
            "iid": iid})


    cursor.execute("SELECT new_price, date_effective FROM Ascott_InvMgmt.PriceChange WHERE item = '{}';".format(iid))

    price = cursor.fetchall()
    pricechanges = []
    if price == ():
        pricechanges.append({
            "iid":iid,
            "new_price": 0,
            "date_effective": 0})
    else:

        for item in price:
            pricechanges.append({
                "iid":iid,
                "new_price": item[0],
                "date_effective": item[1]})

    try:
        if r != []:
            return render_template('item.html', item = r, pricechanges = pricechanges)
        else:
            return render_template('item.html', item = r, pricechanges = pricechanges)
    except:
        return render_template('item.html', item = r, pricechanges = None)


@application.route('/<lang_code>/review/<category>')
def category(category):

    # user authentication
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))
    if session['role'] != "supervisor":
        return redirect(url_for("scanner", lang_code=get_locale()))


    category = category
    itemtype = getAllInventory(category)
    return render_template('category.html',
        category=category,
        itemtype=itemtype,
        role = session['role'],
        user = session['username'])


@application.route('/<lang_code>/storeroom/<storeroom>')
def storeroom(storeroom):

    # user authentication
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))
    if session['role'] != "supervisor":
        return redirect(url_for("scanner", lang_code=get_locale()))

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT tid FROM TagInfo WHERE storeroom='{}';".format(storeroom))
    tags = cursor.fetchall()[0]

    items = {}

    for t in tags:
        cursor.execute("SELECT iid, name, picture, reorder_pt, qty_left, out_by FROM view_item_locations WHERE tag={}".format(t))
        data = cursor.fetchall()
        for d in data:
            if d[0] in items.keys():
                items[d[0]]['qty_left'] += d[4]
            else:
                items[d[0]] = {
                    'name':d[1].encode('ascii'),
                    'picture':d[2].encode('ascii'),
                    'reorder_pt':d[3],
                    'qty_left':d[4],
                    'unit':d[5].encode('ascii')
                }

    return render_template('storeroom.html',
        storename = storeroom,
        items = items,
        user = session['username'],
        role = session['role'])

@application.route('/<lang_code>/logs')
def logs():

    # user authentication
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))
    if session['role'] != "supervisor":
        return redirect(url_for("scanner", lang_code=get_locale()))

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
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))

    return render_template('scanner.html')

# RA shelf view
@application.route('/<lang_code>/shelves/<tag_id>', methods=['GET', 'POST'])
def shelf(tag_id):

    # user authentication
    if not auth():
        session['next'] = request.url
        return redirect(url_for("login", lang_code=get_locale()))

    cursor = mysql.connect().cursor()
    items = inventoryQuick(tag_id)
    cursor.execute("""SELECT tname FROM TagInfo WHERE tid={};""".format(tag_id))
    tagName = cursor.fetchone()[0].encode('ascii')

    if request.method == 'POST':
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form_data = request.form
        user = session['username']

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            for item, info in form_data.iterlists():
                iid = item
                inputQty = int(info[0])
                action = info[1]

                updateSuccess = stockUpdate(iid, tag_id, inputQty, user, action, now)
            flash(updateSuccess[0], updateSuccess[1])
            return redirect(url_for("scanner", lang_code=get_locale()))

        except Exception as e:
            print("CART ERROR: %s" % e)
            flash('Oops! Something went wrong :(', 'danger')

    return render_template('shelf.html', things=items,
        role = session['role'],
        user = session['username'],
        location = tag_id,
        tagName = tagName)


@application.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login", lang_code=get_locale()))


@application.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', error=e), 404

@application.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html', error=e), 500

## testing
if __name__ == '__main__':
    application.run()
