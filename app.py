from flask import Flask
from flask import send_from_directory
from flask import request, session, flash
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from os import listdir
from werkzeug.utils import secure_filename
import os

#login
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "123"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/home')
def inicio():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        #return render_template('home.html', username=session['username'])
        return render_template("inicio.html")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
# @app.route('/')
# def index():
#     return redirect(url_for('inicio'))

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        #return render_template('home.html', username=session['username'])
        return redirect(url_for('inicio'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
  
@app.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('perfil.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Ruta para '/hoteles'
@app.route('/hoteles')
def hoteles():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        #return render_template('home.html', username=session['username'])
        return render_template('hoteles.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    

@app.route('/hoteles/avanty')
def hotelesavanty():
    return render_template('hotelavanty.html')

@app.route('/hoteles/sanjose')
def hotelessanjose():
    return render_template('hotelsanjose.html')

@app.route('/hoteles/luxury')
def hotelesluxury():
    return render_template('hotelluxury.html')

@app.route('/hoteles/villasol')
def hotelesvillasol():
    return render_template('hotelvillasol.html')

@app.route('/hoteles/mora')
def hotelesmora():
    return render_template('hotelmora.html')


@app.route('/Restaurantes')
def restaurantes():
    return render_template('restaurantes.html')

# Manejar error 404 (Página no encontrada)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404

# rutas restaurantes 
@app.route('/restaurantes/pizzeria')
def pizzeria():
    return render_template('pizzeria.html')

@app.route('/restaurantes/sushi')
def sushi():
    return render_template('sushi.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
