from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginFormAdmin(FlaskForm):
    adminname = StringField('admin',
                           validators=[DataRequired(message='Campo requerido')])
    password = PasswordField('Contraseña',
                             validators=[DataRequired(message='Campo requerido')])
    remember = BooleanField('Recordar')
    submit = SubmitField('Ingresar')


