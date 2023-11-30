from flask import Blueprint


restaurante = Blueprint('restaurante', __name__,template_folder='templates', static_folder='static/css')


from . import routes