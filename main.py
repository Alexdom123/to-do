from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import url_for
from flask import redirect

'''from flaskext.mysql import MySQL
mysql = MySQL()
mysql.init_app(app)

cursor = mysql.get_db().cursor()'''

import form

app = Flask(__name__)
'''app.config["MYSQL_DATABASE_HOST"]
app.config["MYSQL_DATABASE_PORT"]
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "to_do"'''

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/newmateria')
def materia():
  form_list = form.ListaForm()
  return render_template('newmateria.html', form = form_list)

@app.route('/materiaward')
def materiaward():
  return render_template('materiaward.html')

@app.route('/llenartareas')
def llenartareas():
  form_tareas = form.Llenartarea()
  return render_template('llenartareas.html', form = form_tareas)

app.run(debug= True, port= 8000)