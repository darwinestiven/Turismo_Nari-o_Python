from flask import render_template
from . import error


@error.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404
