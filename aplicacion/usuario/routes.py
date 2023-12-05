from flask import session, flash
from flask import redirect
from flask import url_for
from flask import render_template
from .forms import RegistrationForm
from .forms import LoginForm
from . import usuario
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
@usuario.route('/login/', methods=['GET', 'POST'])
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
                session['role'] = 'user'
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('home.inicio'))
            else:
                flash('Usuario o Contraseña incorrecta', 'danger')
        else:
            flash('Usuario o Contraseña incorrecta', 'danger')

    return render_template('login.html', form=form)
  
@usuario.route('/register', methods=['GET', 'POST'])
def register():
    try:
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
                return redirect(url_for('usuario.login'))

        return render_template('register.html', form=form)

    except psycopg2.Error as e:
        conn.rollback()  # Deshacer cualquier cambio en la base de datos en caso de error
        flash(f'Error de base de datos: {e}')
    except Exception as e:
        flash(f'Error desconocido: {e}')

    return render_template('register.html', form=form)
   
   
@usuario.route('/logout')
def logout():
   cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Remove session data, this will log the user out
   session['loggedin'] = False
   session.pop('id', None)
   session.pop('username', None)
   cursor.execute("DELETE FROM carrito")
   conn.commit()
   # Redirect to login page
   return redirect(url_for('usuario.login'))
  
@usuario.route('/profile')
def profile(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('perfil.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('usuario.login'))
