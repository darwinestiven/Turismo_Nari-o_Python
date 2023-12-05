from flask import render_template
from flask import redirect
from flask import url_for
from . import home

import psycopg2 #pip install psycopg2 
import psycopg2.extras

from flask import g

#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

contador_reservas = 0
@home.route('/')
def inicio():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT COUNT(*) FROM carrito")
    contador_reservas = cursor.fetchone()[0]
    # Establecer el valor del contador_reservas en el contexto g
    g.contador_reservas = contador_reservas
    return render_template("inicio.html", contador_reservas=contador_reservas)

@home.route('/home/laguna')
def laguna():
    return render_template("laguna.html")

@home.route('/home/bocana')
def bocana():
    return render_template("bocana.html")

