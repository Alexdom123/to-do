from wtforms import Form
from wtforms import StringField, TextField
from wtforms.fields.html5 import EmailField
from wtforms import HiddenField
from wtforms import validators
from wtforms import PasswordField

def length_honeypot(form, field):
	if  len(field.data) > 0:
		raise validators.ValidationError('El campo debe estar vacio.')

class CommentForm(Form):
	"""docstring for ClassName"""
	#username = StringField('Username', [validators.length(min=4, max=25, message='Ingrese un usuario valido')])
	username = StringField('Username', [validators.DataRequired()])
	email = EmailField('Email', [validators.DataRequired()])
	comment = TextField('Comentario', [validators.DataRequired()])
	comment = TextField('Comentario')
	honeypot = HiddenField('', [length_honeypot])

class LoginForm(Form):
	usuario = StringField('Usuario', [validators.DataRequired])
	contraseña = PasswordField('Contraseña', [validators.DataRequired])

class ListaForm(Form):
	materia = StringField('Materia', [validators.DataRequired])
	

class Llenartarea(Form):
	tarea = StringField('', [validators.DataRequired])
	fecha = StringField('', [validators.DataRequired])



		