from flask import Flask
from .home import home
from .error import error
from .hotel import hotel
from .usuario import usuario
from .pueblos import pueblos
from .restaurante import restaurante
from flask_sqlalchemy import SQLAlchemy


app = Flask (__name__)

# Configuration for the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/seminario'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This suppresses a warning

db = SQLAlchemy(app) 

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_pyfile('config/configuracion.cfg')
app.register_blueprint(home)
app.register_blueprint(error)
app.register_blueprint(hotel)
app.register_blueprint(usuario)
app.register_blueprint(pueblos)
app.register_blueprint(restaurante)


