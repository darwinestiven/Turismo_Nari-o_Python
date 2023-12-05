from flask import render_template
from . import restaurante

import psycopg2 #pip install psycopg2 
import psycopg2.extras

from flask import g

DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

contador_reservas = 0

@restaurante.route('/Restaurantes')
def restaurantes():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
     # Actualizar el contador_reservas con la cantidad actual de tuplas en la tabla reservas
    cursor.execute("SELECT COUNT(*) FROM carrito")
    contador_reservas = cursor.fetchone()[0]

    # Establecer el valor del contador_reservas en el contexto g
    g.contador_reservas = contador_reservas
    return render_template('restaurantes.html',contador_reservas=contador_reservas)

# Manejar error 404 (Página no encontrada)

# rutas restaurantes 
@restaurante.route('/restaurantes/pizzeria')
def pizzeria():
    return render_template('pizzeria.html')

@restaurante.route('/restaurantes/sushi')
def sushi():
    return render_template('sushi.html')

