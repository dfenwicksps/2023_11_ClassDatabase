# This is a simple register and login Flask app
# A user can register and login with a username and password
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3  # for database
import bcrypt  # for password hashing

app = Flask(__name__)  # create an instance of the Flask class
app.secret_key = 's3cr3t'  # set the secret key for the session (used to encrypt session data) - this should be a long random string
# the secret key should be stored in a separate file and imported, CSRF protection should also be enabled

def init_db():  # create the database if it doesn't exist
    with app.app_context():  # app.app_context() pushes an application context, which is required to access current_app
        db = sqlite3.connect('userstest.db')  # create a connection to the database
        cursor = db.cursor()  # create a cursor object to execute SQL statements
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)''')  # create a table if it doesn't exist
        db.commit()  # commit the changes

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

@app.route('/')  # route() decorator binds a function to a URL
def home():  # this function is executed when the user visits the home page
    '''if 'user' not in session:
        return redirect(url_for('login'))'''
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # get the password from the form
        hashed_password = hash_password(password)  # hash the password
        try:
            with sqlite3.connect('userstest.db') as db:  # create a connection to the database
                cursor = db.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))  # insert the username and hashed password into the database
                db.commit()  # commit the changes
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))  # redirect the user to the login page
        except sqlite3.IntegrityError:  # if the username already exists in the database then an IntegrityError will be raised
            flash('Username already exists!', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # get the password from the form (this is the password entered by the user)
        with sqlite3.connect('userstest.db') as db:  # create a connection to the database
            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))  # select the user from the database where the username matches the username entered by the user
            user = cursor.fetchone()  # fetch the user
            if user and check_password(user[1], password):  # if the user exists and the password entered by the user matches the hashed password in the database
                session['user'] = user[0]  # set the session user to the username
                return redirect(url_for('home'))  # redirect the user to the home page
            else:
                flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
#  This is a simple register and login Flask app