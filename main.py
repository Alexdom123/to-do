from flask import Flask,render_template, request, make_response, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import form

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'to_do'
mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/main_materia')
def main_materia():
  return render_template('main_materia.html')

@app.route('/addmateria',methods=['POST'])
def addmateria():
  if request.method == 'POST':
    materia = request.form['materia']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO materias (materia) VALUES (%s)", (materia,))
    mysql.connection.commit()
    return redirect(url_for('main_materia'))

@app.route('/main_tarea')
def llenartareas():
  return render_template('main_tarea.html')

"""@app.route('addtarea')
def addtarea():"""
  

app.run(debug= True, port= 8000)