from flask import session, flash
from flask import redirect
from flask import url_for
from flask import render_template
from .forms import LoginFormAdmin
from . import admin
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"


from flask import jsonify

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@admin.route('/loginadmin/', methods=['GET', 'POST'])
def loginadmin():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = LoginFormAdmin()

    if form.validate_on_submit():
        adminname = form.adminname.data
        password = form.password.data

        cursor.execute('SELECT * FROM admin WHERE adminname = %s', (adminname,))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']

            if password_rs == password: 
                session['loggedin'] = True
                session['adminname'] = account['adminname']
                session['role'] = 'admin'
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('home.inicio'))
            else:
                flash('Usuario o Contraseña incorrecta', 'danger')
        else:
            flash('Usuario o Contraseña incorrecta', 'danger')

    return render_template('loginadmin.html', form=form)

@admin.route('/logoutadmin')
def logoutadmin():
    # Remove session data, this will log the user out
   session['loggedin'] = False
   session.pop('adminname', None)
   session.clear()
   # Redirect to login page
   return redirect(url_for('admin.loginadmin'))
  
@admin.route('/profileadmin')
def profileadmin(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM admin WHERE adminname = %s', [session['adminname']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('perfiladmin.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('admin.loginadmin'))



#VISTAS DE RESERVA
@admin.route('/infoReserva', methods=['GET'])
def infoReservas():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Obtén los datos necesarios de la base de datos
    cursor.execute('SELECT id_res, nom_hotel, cant_hab, fecha_ini, fecha_sal, precio_hot, dias_tot, precio_tot FROM reservas')
    reservas_data = cursor.fetchall()

    return render_template('infoReservas.html', reservas=reservas_data)



#ELIMINAR RESERVA

@admin.route('/eliminar_readmin/<int:id>/', methods=['GET'])
def eliminar_readmin(id):
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservas WHERE id_res = %s", (id,))
    conn.commit()

    # Después de eliminar, redirige a la página de reservas actualizada
    return redirect(url_for('admin.infoReservas'))

#VISTAS DE RESERVA
@admin.route('/infoReservajs', methods=['GET'])
def infoReservasjs():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Obtén los datos necesarios de la base de datos
    cursor.execute('SELECT id_res, nom_hotel, cant_hab, fecha_ini, fecha_sal, precio_hot, dias_tot, precio_tot FROM reservas')
    reservas_data = cursor.fetchall()

    return jsonify({'infoReservasjs': reservas_data})

   
