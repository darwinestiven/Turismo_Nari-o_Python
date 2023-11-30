from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo



class RegistrationForm(FlaskForm): 
    fullname = StringField('Nombre',
                           validators=[DataRequired(message='Campo requerido')])
    email = StringField('Email', 
                        validators=[DataRequired(message='Campo requerido'),
                                    Email(message='Dirección de correo electrónico no válida')])
    username = StringField('Usuario', 
                           validators=[DataRequired(message='Campo requerido')])
    password = PasswordField('Contraseña', 
                            validators=[DataRequired(message='Campo requerido')])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(message='Campo requerido'),
                                                 EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrar')
    
class LoginForm(FlaskForm):
    username = StringField('Usuario',
                           validators=[DataRequired(message='Campo requerido')])
    password = PasswordField('Contraseña',
                             validators=[DataRequired(message='Campo requerido')])
    remember = BooleanField('Recordar')
    submit = SubmitField('Ingresar')

