from flask import Flask,render_template, request, make_response, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import form
import bcrypt #librería para encriptacion de datos
import re #alchile no sé pa k es

app = Flask(__name__)
app.secret_key = 'eres secreto de amor'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'to_do'
mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('main_entrar.html')

@app.route('/home')
def home():
  # Revisa si el usuario está logueado
  if 'loggedin' in session:
    # El usuario esta logueado y le mostramos el home
    return render_template('index.html', username=session['username'])
  #El usuario no esta logueado, redireccionamos al inicio de sesion
  return redirect(url_for('/'))

@app.route('/', methods=['POST'])
def login():
  username = request.form['txtusuario']
  passwordPlano = request.form['txtpassword']
  cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cur.execute("SELECT * FROM usuarios WHERE nombre='" + username + "'")
  if cur is not None:
    account = cur.fetchone()
    password = account['password']
    # Comparamos la password con la password hasheada
    if bcrypt.checkpw(passwordPlano.encode('utf-8'), password.encode('utf-8')):
      # si la contraseña plana es igual a la encriptada...
      if account:
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['nombre']
        return redirect(url_for('home'))
      else:
        flash ('Usuario o Password incorrectos!')
        return redirect(url_for('/'))

@app.route('/logout')
def logout():
  # Elimina la informacion de la sesion, esto sacara al usuario
  session.pop('loggedin', None)
  session.pop('id', None)
  session.pop('username', None)
  # Redireccionamos a la pagina del login
  return redirect(url_for('login'))

@app.route('/main_materia')
def main_materia():
  return render_template('main_materia.html', username=session['username'])

@app.route('/addmateria',methods=['POST'])
def addmateria():
  if 'loggedin' in session:
    if request.method == 'POST':
      materia = request.form['materia']
      usuario = session['id']
      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO materias (materia, id) VALUES (%s, %s)", (materia, usuario))
      mysql.connection.commit()
      flash ('Materia registrada correctamente!')
      return redirect(url_for('main_materia'))  

@app.route('/main_registro')
def main_registro():
  return render_template('main_registro.html')

@app.route('/addregistro', methods=['POST'])
def registro():
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
      flash ('La cuenta ya existe!')
    elif not nombre or not password or not correo or not institucion:
      flash ('Por favor, llena el formulario!')
    else:
      # La cuenta no existe y la informacion del formulario es valida, se inserta el usuario en la bd
      cur.execute("INSERT INTO usuarios(nombre, correo, institucion, password) VALUES(%s, %s, %s, %s)", (nombre, correo, institucion, encriptada,))
      mysql.connection.commit()
      #cerramos la conexión a la bd
      mysql.connection.close()
      print("S U C C E S S")
      flash ('Registrado con éxito!')
      return redirect(url_for('login'))
  elif request.method == 'POST': #Si el formulario esta vacio
    flash ('Por favor introduce todos los datos')
  return render_template('main_registro.html')

@app.route('/mis_materias')
def mis_materias():
  if 'loggedin' in session:
    usuario = session['id']
    idUsuario = str(usuario)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materias where id=" + idUsuario)
    data = cur.fetchall()
    cur.close()
    return render_template('mis_materias.html', materias = data, username=session['username'])

@app.route('/delete_materia/<string:id>', methods=['POST', 'GET'])
def deleteM(id):
  cur = mysql.connection.cursor()
  cur.execute("DELETE FROM materias where idMateria = {0}".format(id))
  mysql.connection.commit()
  
  return redirect(url_for('mis_materias'))

@app.route('/edit_materia/<id>', methods = ['POST', 'GET'])
def get_materia(id):
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM materias WHERE idMateria = %s", [id])
  data = cur.fetchall()
  cur.close()
  print(data[0])
  return render_template('edit_materias.html', materia = data[0], username=session['username'])

@app.route('/update/<id>', methods = ['POST'])
def actualizar_materia(id):
  if request.method == 'POST':
    materia = request.form['materia']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE materias SET materia = %s WHERE idMateria = %s", (materia, id))
    mysql.connection.commit()
    
  return redirect(url_for('mis_materias'))

@app.route('/main_tarea')
def main_tarea():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM materias")
  data = cur.fetchall()
  cur.close()
  return render_template('main_tarea.html', materias = data, username=session['username'])

@app.route('/addtarea',methods=['POST'])
def addtarea():
  if request.method == 'POST':
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    creada = request.form['creada']
    entrega = request.form['entrega']
    idmateria = request.form['materia']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tareas (titulo, descripcion, creada, entrega, idMateria) VALUES (%s, %s, %s, %s,%s)", (titulo, descripcion, creada, entrega, idmateria))
    mysql.connection.commit()
    return redirect(url_for('main_tarea'))  

@app.route('/mis_tareas')
def mis_tareas():
  cur = mysql.connection.cursor()
  cur.execute("SELECT tareas.idTarea, tareas.titulo, tareas.descripcion, tareas.creada, tareas.entrega, materias.materia, materias.idMateria FROM tareas INNER JOIN materias WHERE tareas.idMateria = materias.idMateria")
  data = cur.fetchall()
  cur.close()
  return render_template('mis_tareas.html', tareas = data)

app.run(debug= True, port= 8000)
