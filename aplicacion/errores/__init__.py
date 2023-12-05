from flask import Blueprint


errores = Blueprint('errores',__name__, template_folder ='templates', static_folder='static/css')

from . import routes