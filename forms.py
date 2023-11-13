from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from flask_wtf.file import FileAllowed


class FormCalculadora(FlaskForm):
    num1 = IntegerField("Número1",
                        validators=[DataRequired(
                            "Tiene que introducir un número entero")])
    num2 = IntegerField("Número2",
                        validators=[DataRequired(
                            "Tiene que introducir un número entero")]
                        )
    operador = SelectField("Operador",
                           choices=[("+", "Sumar"), ("-", "Resta"),
                                    ("*", "Multiplicar"), ("/", "Dividir")])
    submit = SubmitField('Calcular by WTF')


class UploadForm(FlaskForm):
    photo = FileField('Selecciona imagen:',
                      validators=[FileRequired("Es necesario seleccionar un "
                                               "archivo de imagen"),
                                  FileAllowed(['jpg', 'png'],
                                              "Archivos válidos jpg o png "
                                              "únicamente")])
    submit = SubmitField('Subir imagen')
