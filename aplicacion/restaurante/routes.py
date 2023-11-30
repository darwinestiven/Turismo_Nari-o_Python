from flask import render_template
from . import restaurante



@restaurante.route('/Restaurantes')
def restaurantes():
    return render_template('restaurantes.html')

# Manejar error 404 (Página no encontrada)

# rutas restaurantes 
@restaurante.route('/restaurantes/pizzeria')
def pizzeria():
    return render_template('pizzeria.html')

@restaurante.route('/restaurantes/sushi')
def sushi():
    return render_template('sushi.html')

