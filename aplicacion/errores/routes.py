from flask import render_template
from . import errores
from flask import Flask
from flask import request
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from os import listdir
from werkzeug.utils import secure_filename


@errores.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404

