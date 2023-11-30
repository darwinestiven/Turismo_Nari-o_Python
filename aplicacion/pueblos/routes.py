from flask import render_template
from . import pueblos


@pueblos.route('/pueblos/sandona')
def sandona():
    return render_template('sandona.html')
