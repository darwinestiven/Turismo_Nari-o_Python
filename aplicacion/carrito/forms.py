from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import DateInput
from datetime import datetime
import psycopg2
import psycopg2.extras

#login
DB_HOST = "localhost"
DB_NAME = "seminario"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


class carritoForm(FlaskForm):
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired()], widget=DateInput())
    fecha_salida = DateField('Fecha de Salida', format='%Y-%m-%d', validators=[DataRequired()], widget=DateInput())
    cantidad_hab = IntegerField('Cantidad de Habitaciones', validators=[DataRequired(message='Campo requerido')])
    submit = SubmitField('Confirmar')

    def validate_fecha_inicio(self, field):
        if field.data < datetime.today().date():
            raise ValidationError('La fecha de inicio no puede ser anterior a la fecha actual.')

    def validate_cantidad_hab(self, field):
        if field.data < 0:
            raise ValidationError('La cantidad de habitaciones no puede ser negativa.')


    def validate_fecha_salida(self, field):
        if field.data <= self.fecha_inicio.data:
            raise ValidationError('La fecha de salida no puede ser anterior o igual a la fecha de inicio.')

    