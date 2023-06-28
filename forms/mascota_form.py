from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class mascotaForm(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired()])
    raza = StringField('raza', validators=[DataRequired()])
    edad = StringField('edad', validators=[DataRequired()])
    nivel_de_actividad = StringField('nivel_actividad', validators=[DataRequired()])
    peso = StringField('peso', validators=[DataRequired()])
    entorno = StringField('entorno', validators=[DataRequired()])
    submit = SubmitField('Submit')

class preguntaForm(FlaskForm):
    pregunta = StringField('pregunta', validators=[DataRequired()])
    submit = SubmitField('Submit')
