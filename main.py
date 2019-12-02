from flask import Flask,render_template, request, make_response, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import form
import bcrypt #librería para encriptacion de datos

app = Flask(__name__)
app.secret_key = 'eres secreto de amor'
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
    cur.execute("INSERT INTO materias (materia) VALUES (%s)", [materia])
    mysql.connection.commit()
    flash('Materia agregada correctamente')
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
      flash ('You have successfully registered!')
      return redirect(url_for('main_entrar'))
  elif request.method == 'POST': #Si el formulario esta vacio
    flash ('Por favor introduce todos los datos')
  return render_template('main_registro.html')

@app.route('/mis_materias')
def mis_materias():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM materias")
  data = cur.fetchall()
  cur.close()
  return render_template('mis_materias.html', materias = data)

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
  return render_template('edit_materias.html', materia = data[0])

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
  return render_template('main_tarea.html', materias = data)

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
