
from flask import render_template
from . import hotel
from flask import session, flash
from flask import redirect
from flask import url_for
from .forms import HotelForm, EditarHotelForm
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

from flask import request
from werkzeug.utils import secure_filename
import os

from flask import current_app

from wtforms.widgets import HiddenInput

from flask_paginate import Pagination, get_page_args

from flask import g


#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

contador_reservas = 0

#Ruta agregar hotel
@hotel.route('/registerHotel', methods=['GET', 'POST'])
def registerHotel():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = HotelForm()

    if form.validate_on_submit():
        id = form.id.data
        nombreH = form.nombreH.data
        descripcionH = form.descripcionH.data
        precioH = form.precioH.data
        direccionH = form.direccionH.data
        disponibilidadH = form.disponibilidadH.data
        imagen = form.imagen.data

        # Validar si se proporcionó una imagen
        form = HotelForm()  # carga request.form y request.file
        if form.validate_on_submit():
            f = form.imagen.data
            filename = secure_filename(f.filename)
            f.save(current_app.root_path + "/static/img/" + filename)
   

        cursor.execute('SELECT * FROM hoteles WHERE id = %s', (id,))
        account = cursor.fetchone()

        if account:
            flash('El hotel ya existe!')
        else:
            cursor.execute("INSERT INTO hoteles (id, nombreH, descripcionH, precioH, direccionH, disponibilidadH, imagen) VALUES (%s,%s,%s,%s,%s,%s,%s)", (id, nombreH, descripcionH, precioH, direccionH, disponibilidadH, filename))
            conn.commit()
            flash('Se ha registrado exitosamente!')
            return redirect(url_for('hotel.hoteles'))
        

    return render_template('registerHotel.html', form=form)



# Mostrar hoteles
@hotel.route('/hoteles', methods=['GET', 'POST'])
def hoteles():
    global contador_reservas  # Declarar la variable como global
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Obtén el número de página actual
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    
    # Obtén todos los hoteles y el total de hoteles

    cursor.execute('SELECT * FROM hoteles')
    hoteles = cursor.fetchall()
    total_hoteles = len(hoteles)

    #pagination_hoteles = get_hoteles(offset=offset, per_page=4)
    # Calcula el número total de páginas
    pagination = Pagination(page=page, per_page=4, total=total_hoteles,
                            css_framework='bootstrap4',record_name='hoteles')
    

    #Limita los hoteles según la paginación
    start = (page - 1) * per_page
    end = start + per_page
    hoteles_paginados = hoteles[start:end]
    
    cursor.execute("SELECT COUNT(*) FROM carrito")
    contador_reservas = cursor.fetchone()[0]
    # Establecer el valor del contador_reservas en el contexto g
    g.contador_reservas = contador_reservas

    # Mostrar la página de hoteles con la lista de hoteles paginados
    return render_template('hoteles.html', hoteles=hoteles_paginados, pagination=pagination, contador_reservas=contador_reservas)



# Ruta para la edición de hoteles
@hotel.route('/editarHotel/<int:id>', methods=['GET', 'POST'])
def editarHotel(id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = EditarHotelForm()

    if request.method == 'GET':
        # Obtener los datos del hotel para prellenar el formulario
        cursor.execute('SELECT * FROM hoteles WHERE id = %s', (id,))
        hotel_data = cursor.fetchone()

        if hotel_data:
            # Preencher el formulario con los datos del hotel
            form.id.data = hotel_data[0]
            form.nombreH.data = hotel_data[1]
            form.descripcionH.data = hotel_data[2]
            form.precioH.data = hotel_data[3]
            form.direccionH.data = hotel_data[4]
            form.disponibilidadH.data = hotel_data[5]
            form.imagen.data = hotel_data[6]
            # Puedes omitir la imagen ya que no se debería mostrar en el formulario de edición


    elif request.method == 'POST' and form.validate_on_submit():
        # Procesar el formulario enviado para actualizar el hotel
        # (código similar al de la función registerHotel)

        #id = form.id.data
        nombreH = form.nombreH.data
        descripcionH = form.descripcionH.data
        precioH = form.precioH.data
        direccionH = form.direccionH.data
        disponibilidadH = form.disponibilidadH.data
        imagen = form.imagen.data

        # Validar si se proporcionó una imagen
        form = HotelForm()  # carga request.form y request.file
        if form.validate_on_submit():
            f = form.imagen.data
            filename = secure_filename(f.filename)
            f.save(current_app.root_path + "/static/img/" + filename)
   
        cursor.execute("UPDATE hoteles SET nombreH=%s, descripcionH=%s, precioH=%s, direccionH=%s, disponibilidadH=%s, imagen=%s WHERE id=%s", (nombreH, descripcionH, precioH, direccionH, disponibilidadH, filename, id))
        conn.commit()

        flash('Hotel actualizado exitosamente!')
        return redirect(url_for('hotel.hoteles'))

    return render_template('editarHotel.html', form=form)



# Nueva ruta para eliminar un hotel
@hotel.route('/eliminarHotel/<int:id>', methods=['GET', 'POST'])
def eliminarHotel(id):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Obtener los datos del hotel para mostrar en la página de confirmación
    cursor.execute('SELECT * FROM hoteles WHERE id = %s', (id,))
    hotel_data = cursor.fetchone()

    if not hotel_data:
        flash('Hotel no encontrado.')
        return redirect(url_for('hotel.hoteles'))

    if request.method == 'POST':
        # Eliminar el hotel de la base de datos
        cursor.execute('DELETE FROM hoteles WHERE id = %s', (id,))
        conn.commit()
        flash('Hotel eliminado exitosamente!')
        return redirect(url_for('hotel.hoteles'))

    return render_template('eliminarHotel.html', hotel=hotel_data)

