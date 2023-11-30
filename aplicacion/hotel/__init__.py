from flask import Blueprint

hotel = Blueprint('hotel', __name__, template_folder='templates', static_folder='static/css')

from . import routes