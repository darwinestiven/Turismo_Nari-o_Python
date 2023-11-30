from flask import render_template
from flask import redirect
from flask import url_for
from . import home


@home.route('/')
def inicio():
    return render_template("inicio.html")

@home.route('/home/laguna')
def laguna():
    return render_template("laguna.html")

@home.route('/home/bocana')
def bocana():
    return render_template("bocana.html")

