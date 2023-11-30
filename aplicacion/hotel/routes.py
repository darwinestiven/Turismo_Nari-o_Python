
from flask import render_template
from . import hotel




# Ruta para '/hoteles'
@hotel.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')


@hotel.route('/hoteles/hotelesavanty')
def hotelavanty():
    # Lógica para la vista de hotelesavanty aquí
    return render_template("hotelavanty.html")

@hotel.route('/hoteles/sanjose')
def hotelessanjose():
    return render_template('hotelsanjose.html')

@hotel.route('/hoteles/luxury')
def hotelesluxury():
    return render_template('hotelluxury.html')

@hotel.route('/hoteles/villasol')
def hotelesvillasol():
    return render_template('hotelvillasol.html')

@hotel.route('/hoteles/mora')
def hotelesmora():
    return render_template('hotelmora.html')


