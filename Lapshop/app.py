from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, create_access_token, get_jwt
import hashlib
import mysql.connector
from datetime import datetime, timedelta
from functools import wraps
import platform

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super' #CAMBIAR ESTO!!!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes = 5)

jwt = JWTManager(app)

# La base de datos que se uso fue la de MySQL WorkBench, 
# para facilitar la comprobacion.
connection_data = {
    'user': 'root',
    'password': 'Charles120Ahoy',
    'host': '127.0.0.1',
    'database': 'laptops'
}

# Funcion para crear un nuevo registro (log)
def log_access(f):
    @wraps(f)
    def create_log(*args, **kwargs):
        # Acceder al token
        token = get_jwt_identity()
        user_id = token  # Obtener el usuario ID
        endpoint = request.endpoint  # Nombre del endpoint accedido
        timestamp = datetime.now() # Fecha de consulta del endpoint
        claims = get_jwt()
        reg_date = datetime.strptime(claims["register_date"],'%Y-%m-%d %H:%M:%S')
        connection = mysql.connector.connect(**connection_data)
        mycursor = connection.cursor()
        new_log_sql = "INSERT INTO endpoint_logs (user_id, endpoint, start_time, register_date) VALUES (%s, %s, %s, %s)" #Consulta para agregar el nuevo registro
        val = (user_id, endpoint, timestamp, reg_date)
        mycursor.execute(new_log_sql, val) #Ejecutar
        connection.commit() #Guardar cambios
        connection.close() #Cerrar conexion
        return f(*args, **kwargs) #Devolver la funcion original
    return create_log

@app.route("/")
def main():
    return "<center><h1>LAPSHOP PRIME</h1></center>"

#endpoint de registro de usuario
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #Si la peticion es POST, obtener los datos del formulario
        username = request.form['username']
        password = request.form['passw'].encode('utf-8')
        #Realizar la conexion a la base de datos
        connection = mysql.connector.connect(**connection_data)
        mycursor = connection.cursor()
        #Buscar el usuario en caso de que este ya exista
        mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = mycursor.fetchone()
        #Si existe en la base de datos
        if user:
            connection.close()
            return jsonify({'mensaje': 'El usuario ya existe'}), 400
        #Caso contrario, encriptar la clave de acceso
        hashed_password = hashlib.sha256(password).hexdigest()
        reg_date = datetime.now()
        #Guardar el usuario en la base de datos
        sql = "INSERT INTO users (username, passw, register_date) VALUES (%s, %s, %s)"
        val = (username, hashed_password, reg_date)
        mycursor.execute(sql, val)
        #Guardar cambios y cerrar conexion
        connection.commit()
        connection.close()
        #Redirigir al usuario a la pagina de inicio de sesión
        return redirect(url_for('login', json=request.form), code=307)

    #Si la solicitud es GET, simplemente renderizar el formulario HTML
    return render_template('register.html')

#endpoint para inicio de sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Si la peticion es POST, obtener los datos de inicio de sesion
        username = request.form['username']
        password = request.form['passw'].encode('utf-8')
        #Abrir la conexion a la base de datos
        connection = mysql.connector.connect(**connection_data)
        #Crear un cursor para interactuar con la base de datos
        mycursor = connection.cursor()
        #Obtener los datos de usuario de la base de datos
        sql = "SELECT * FROM users WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        #Comprobar que se hayan enviado las credenciales correctas
        if user is None or hashlib.sha256(password).hexdigest() != user[2]:
            connection.close()
            return jsonify({"msg": "Credenciales inválidas"}), 401

        time = datetime.now()
        expire = time + timedelta(minutes=5)
        additional_claims = {"user": user[1], "expires_at": expire, "register_date": user[3].strftime('%Y-%m-%d %H:%M:%S')}
        #Crear token de sesión
        access_token = create_access_token(identity=user[0], additional_claims=additional_claims)
        

        #Guardar la sesion en la base de datos
        new_session_sql = "INSERT INTO sessions (user_id, token, browser, os, created_at, expires_at) VALUES (%s, %s, %s,%s,%s,%s)"
        val = (user[0], access_token, request.user_agent.string, platform.system(), time, expire)
        mycursor.execute(new_session_sql, val)
        connection.commit()
        connection.close()
        # Devolver el token de sesion
        return jsonify({
            "Username": user[1],
            "Access_token": access_token,
            "Browser": request.user_agent.string,
            "Operative System": platform.system(),
            "Created_at": time.strftime('%Y-%m-%d %H:%M:%S'),
            "Expired_at": expire.strftime('%Y-%m-%d %H:%M:%S')
        }), 200
    return render_template('login.html')


@app.route("/laptops")
def laptops():
    return "<h1>Catalogo de laptops</h1>"


@app.route("/about/terms-of-use")
def terms():
    return "<h1>Pagina en Mantenimiento</h1>"

@app.route("/about")
def about():
    with open("about.json") as archivo:
        datos = json.load(archivo)
    return datos


#Consultar Todos Laptops
@app.route("/laptops/all")
@jwt_required()
@log_access
def example():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM laptops")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos Fabricantes
@app.route("/manufacturer/all")
@jwt_required()
@log_access
def manufacturer():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM manufacturer")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos Procesadores
@app.route("/processor/all")
@jwt_required()
@log_access
def processor():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM processor")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos Tarjetas Graficas
@app.route("/graphics/all")
@jwt_required()
@log_access
def graphics():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM graphics_card")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos Series
@app.route("/series/all")
@jwt_required()
@log_access
def series():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM series")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos RAM_Sticks
@app.route("/ram/all")
@jwt_required()
@log_access
def ram():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ram_sticks")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos Screens
@app.route("/screens/all")
@jwt_required()
@log_access
def screens():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM screens")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#Consultar Todos Storage_drives
@app.route("/storages/all")
@jwt_required()
@log_access
def storage():
    connection = mysql.connector.connect(**connection_data)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM storage_drives")
    headers=[x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(headers,result)))
    return jsonify(json_data)


#App
if __name__ == '__main__':
    app.run(debug=True)
