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
from forms import RegistrationForm
from forms import LoginForm

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
    return render_template("inicio.html")

@app.route('/home/laguna')
def laguna():
    return render_template("laguna.html")

@app.route('/home/bocana')
def bocana():
    return render_template("bocana.html")
    

@app.route('/')
def home():
    return redirect(url_for('inicio'))
    

@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']

            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('home'))
            else:
                flash('Usuario o Contraseña incorrecta', 'danger')
        else:
            flash('Usuario o Contraseña incorrecta', 'danger')

    return render_template('login.html', form=form)
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = RegistrationForm()

    if form.validate_on_submit():
        fullname = form.fullname.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash('La cuenta ya existe!')
        else:
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, hashed_password, email))
            conn.commit()
            flash('Se ha registrado exitosamente!')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session['loggedin'] = False
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
    
    
        # User is loggedin show them the home page
        #return render_template('home.html', username=session['username'])
        return render_template('hoteles.html')
    # User is not loggedin redirect to login page
    
    

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

@app.route('/pueblos/sandona')
def sandona():
    return render_template('sandona.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
