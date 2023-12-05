from flask import render_template
from . import carrito
from flask import session, flash
from flask import redirect
from flask import url_for
from .forms import carritoForm
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
from datetime import datetime
from wtforms.validators import DataRequired, ValidationError

from wtforms import StringField, SubmitField, IntegerField, DateField
from flask import g

#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Variable global para el contador
contador_reservas = 0

#registrar Fechas a carrito
@carrito.route('/registerCarrito/<int:id>', methods=['GET', 'POST'])
def registerCarrito(id):
    global contador_reservas  # Declarar la variable como global
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    form = carritoForm()

    if form.validate_on_submit():
            
        fecha_inicio = form.fecha_inicio.data
        fecha_salida = form.fecha_salida.data
        cantidad_hab = form.cantidad_hab.data

        id_hotel = id
        
        # Validar que la cantidad de habitaciones sea menor o igual a la disponibilidad del hotel
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT disponibilidadh FROM hoteles where id=%s ", (id_hotel,))
        result = cursor.fetchone()

        
        disponibilidad = result['disponibilidadh']
        if cantidad_hab > disponibilidad:
            flash('La cantidad de habitaciones no puede ser mayor que la disponibilidad del hotel.')
        else:
            cursor.execute("INSERT INTO carrito (fecha_inicio, fecha_salida, cantidad_hab, id_hotel) VALUES (%s, %s, %s, %s)",
                       (fecha_inicio, fecha_salida, cantidad_hab, id_hotel))
            
             # Actualizar el contador_reservas con la cantidad actual de tuplas en la tabla reservas
            
            conn.commit()

            flash('Reserva registrada exitosamente!')
            return redirect(url_for('hotel.hoteles'))

    cursor.execute("SELECT COUNT(*) FROM carrito")
    contador_reservas = cursor.fetchone()[0]   
     # Establecer el valor del contador_reservas en el contexto g
    g.contador_reservas = contador_reservas

    return render_template('registerCarrito.html', form=form, contador_reservas=contador_reservas)



#añadir a carrito
@carrito.route('/reservas/', methods=['GET'])
def reservas():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Obtén los datos necesarios de la base de datos
    cursor.execute("""
        SELECT carrito.id, hoteles.nombreh, carrito.cantidad_hab, carrito.fecha_inicio, carrito.fecha_salida, hoteles.precioh,
               (carrito.fecha_salida - carrito.fecha_inicio) AS dias_totales,
               (carrito.cantidad_hab * hoteles.precioh * (carrito.fecha_salida - carrito.fecha_inicio)) AS precio_total
        FROM carrito
        INNER JOIN hoteles ON hoteles.id = carrito.id_hotel
    """)
    reservas_data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM carrito")
    contador_reservas = cursor.fetchone()[0]

    # Establecer el valor del contador_reservas en el contexto g
    g.contador_reservas = contador_reservas

    return render_template('reservas.html', reservas=reservas_data, contador_reservas=contador_reservas)



#eliminar reserva

@carrito.route('/eliminar_reserva/<int:id>/', methods=['GET'])
def eliminar_reserva(id):
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito WHERE id = %s", (id,))
    conn.commit()

    # Después de eliminar, redirige a la página de reservas actualizada
    return redirect(url_for('carrito.reservas'))


#hacer reserva
@carrito.route('/hacer_reserva', methods=['GET', 'POST'])
def hacer_reserva():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
        SELECT carrito.id, hoteles.nombreh, carrito.cantidad_hab, carrito.fecha_inicio, carrito.fecha_salida, hoteles.precioh,
               (carrito.fecha_salida - carrito.fecha_inicio) AS dias_totales,
               (carrito.cantidad_hab * hoteles.precioh * (carrito.fecha_salida - carrito.fecha_inicio)) AS precio_total
        FROM carrito
        INNER JOIN hoteles ON hoteles.id = carrito.id_hotel
    """)
    result = cursor.fetchall()

    for row in result:
        cursor.execute("""
            INSERT INTO reservas (id_res, nom_hotel, cant_hab, fecha_ini, fecha_sal, precio_hot, dias_tot, precio_tot)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    # Commit the changes to the database

    for row in result:
    # Restar la cantidad de habitaciones reservadas de la disponibilidad total
        cursor.execute("UPDATE hoteles SET disponibilidadh = disponibilidadh - %s WHERE hoteles.nombreh = %s",
                   (row[2], row[1]))

    conn.commit()

    #cursor = conn.cursor()
    cursor.execute("DELETE FROM carrito")
    conn.commit()
    #print(result)


    return redirect(url_for('carrito.reservas'))
