from flask import Flask,render_template, request, make_response, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import form
import bcrypt #librería para encriptacion de datos

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'to_do'
mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/entrar')
def main_entrar():
  return render_template('main_entrar.html')

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

@app.route('/main_registro')
def main_registro():
  return render_template('main_registro.html')

@app.route('/addregistro', methods=['POST'])
def registro():
  mensaje = '' #para escribir dentro si algo malo sucede
  if request.method == 'POST' and 'nombre' in request.form and 'password' in request.form and 'correo' in request.form and 'institucion' in request.form:
    nombre = request.form['nombre']
    password = request.form['password'].encode('UTF-8')
    encriptada = bcrypt.hashpw(password, bcrypt.gensalt())
    correo = request.form['correo'] 
    institucion = request.form['institucion']
    # Revisa si la cuenta ya existe usando MySQL
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE nombre = %s', (nombre,))
    account = cur.fetchone()
    # Si la cuenta existe muestra un mensaje de errir
    if account:
      mensaje = 'La cuenta ya existe!'
    elif not nombre or not password or not correo or not institucion:
      mensaje = 'Por favor, llena el formulario!'
    else:
      # La cuenta no existe y la informacion del formulario es valida, se inserta el usuario en la bd
      cur.execute("INSERT INTO usuarios(nombre, correo, institucion, password) VALUES(%s, %s, %s, %s)", (nombre, correo, institucion, encriptada,))
      mysql.connection.commit()
      #cerramos la conexión a la bd
      mysql.connection.close()
      print("success")
      mensaje = 'You have successfully registered!'
      return redirect(url_for('main_registro', mensaje=mensaje))
  elif request.method == 'POST': #Si el formulario esta vacio
    mensaje = 'Por favor introduce todos los datos'
  return render_template('main_registro.html', mensaje=mensaje)

@app.route('/main_tarea')
def llenartareas():
  return render_template('main_tarea.html')
  

app.run(debug= True, port= 8000)