from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, abort
# from  flask_mysqldb import MySQL
import pymysql
from flask_cors import CORS

# import MySQLdb.cursors
import re
from datetime import timedelta

app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = 'thesecretkey'
app.permanent_session_lifetime = timedelta(minutes=10)

# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'test'
# To connect MySQL database
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password="root@123",
    db='449_db',
)

cur = conn.cursor()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # session.permanent = True
        session.modified = True
        username = request.form['username']
        password = request.form['password']
        # cursor = cur.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        # conn.commit()
        account = cur.fetchone()
        # account = json.dumps(account)
        print("Login time acct", account)
        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            # session['id'] = dict(account)[id]
            session['id'] = account[0]
            # session['username'] = account['username']
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg, username=session["username"])
        else:
            msg = 'Incorrect username / password !'
    if request.method == 'GET' and 'loggedin' in session:
        session.modified = True
        return redirect(url_for('index'))
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        # cursor = cur.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE username = % s', (username,))
        account = cur.fetchone()
        # conn.commit()
        print("First time ", account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
                        (username, password, email, organisation, address, city, state, country, postalcode,))
            # cur.commit()
            conn.commit()
            msg = 'You have successfully registered !'
            print("Second time ", account)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/index")
def index():
    session.modified = True
    print("index acct is", session['username'])
    if 'loggedin' in session:
        return render_template("index.html",  username=session['username'])
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        session.modified = True
        # cursor = cur.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE id = % s', (session['id'],))
        account = cur.fetchone()
        print("display acct is", account)
        return render_template("display.html", account=account, username=session['username'])
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        session.modified = True
        # cur.execute('SELECT * FROM accounts WHERE id = % s', (session['id'],))
        # account = cur.fetchone()
        # render_template("update.html", account=account)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            # cursor = cur.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM accounts WHERE username = % s', (username,))
            account = cur.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cur.execute(
                    'UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s',
                    (username, password, email, organisation, address, city, state, country, postalcode,
                     (session['id'],),))
                # cur.commit()
                conn.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg, username=session['username'])
    return redirect(url_for('login'))


# define username and password
USERNAME = 'admin'
PASSWORD = 'admin'


# admin page
# @app.route('/admin')
# def admin():
#     # check if the user is authorized
#     auth = request.authorization
#     print(auth)
#     if not auth or auth.username != USERNAME or auth.password != PASSWORD:
#         # if not authorized, show 401 error page
#         abort(401)
#     # if authorized, show admin page
#     return render_template('admin.html')


def isAdmin(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if (not (session["loggedin"] and session["username"] == 'admin')):
            return render_template('401.html', username=session['username']), 401
        return func(*args, **kwargs)

    return decorated


@app.route("/admin", methods=['POST', 'GET'])
@isAdmin
def admin():
    return render_template("admin.html", username=session['username'])


# 401 error page
@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html', username=session['username']), 401


if __name__ == "__main__":
    app.run(host="localhost", port=int("5200"), debug=True)
