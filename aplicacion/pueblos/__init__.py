from flask import Blueprint


pueblos = Blueprint('pueblos', __name__, template_folder='templates', static_folder='static/css')

from . import routes