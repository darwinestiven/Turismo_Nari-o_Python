from flask import Flask
from .home import home
from .errores import errores
from .hotel import hotel
from .usuario import usuario
from .pueblos import pueblos
from .restaurante import restaurante
from .admin import admin
from .carrito import carrito
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

from flask_mail import Mail


app = Flask (__name__)
app.config['UPLOAD_FOLDER'] = '/aplicacion/static/img'

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'darwinestivendiaz@gmail.com'
app.config['MAIL_PASSWORD'] = 'pvls mmoi krdk evph'
# Otras configuraciones...

mail = Mail(app)

# Configuration for the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/seminario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This suppresses a warning

db = SQLAlchemy(app) 

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_pyfile('config/configuracion.cfg')
app.register_blueprint(home)
app.register_blueprint(errores)
app.register_blueprint(hotel)
app.register_blueprint(usuario)
app.register_blueprint(pueblos)
app.register_blueprint(restaurante)
app.register_blueprint(admin)
app.register_blueprint(carrito)










































































@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error500.html', error_code=500), 500


