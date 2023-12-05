from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, SubmitField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired


class HotelForm(FlaskForm):
    id = IntegerField('ID del Hotel', validators=[DataRequired(message='Campo requerido')])
    nombreH = StringField('Nombre del Hotel', validators=[DataRequired(message='Campo requerido')])
    descripcionH = TextAreaField('Descripción del Hotel', validators=[DataRequired(message='Campo requerido')])
    precioH = DecimalField('Precio del Hotel', validators=[DataRequired(message='Campo requerido')])
    direccionH = StringField('Dirección del Hotel', validators=[DataRequired(message='Campo requerido')])
    disponibilidadH = IntegerField('Disponibilidad del Hotel', validators=[DataRequired(message='Campo requerido')])
    imagen = FileField('Cargar Imagen', validators=[DataRequired(message='Campo requerido')])
    submit = SubmitField('Guardar')


class EditarHotelForm(FlaskForm):
    id = IntegerField('ID del Hotel', validators=[DataRequired(message='Campo requerido')])
    nombreH = StringField('Nombre del Hotel', validators=[DataRequired(message='Campo requerido')])
    descripcionH = TextAreaField('Descripción del Hotel', validators=[DataRequired(message='Campo requerido')])
    precioH = DecimalField('Precio del Hotel', validators=[DataRequired(message='Campo requerido')])
    direccionH = StringField('Dirección del Hotel', validators=[DataRequired(message='Campo requerido')])
    disponibilidadH = IntegerField('Disponibilidad del Hotel', validators=[DataRequired(message='Campo requerido')])
    imagen = FileField('Cargar Imagen', validators=[DataRequired(message='Campo requerido')])
    submit = SubmitField('Guardar')
