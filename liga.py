"""
Este proyecto es una API hecha con Flask que maneja endpoints de 
registro de usuarios e inicio de sesion, ademas de usar JWT para 
autenticar a los usuarios y proporcionar un token de acceso. Esta API proporciona
datos estadisticos de la Liga MX cargados previamente en una base de datos hecha en MySQL. 
"""
import hashlib
import json
from datetime import datetime, timedelta
import platform
from functools import wraps
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, create_access_token
from user_agents import parse

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'chuchogol'

jwt = JWTManager(app)

# Coneccion a la base de datos de mysql
connectionDatabase = {
    'user': 'root',
    'password': 'ligamx',
    'host': 'localhost',
    'database': 'base',
    'auth_plugin': 'mysql_native_password'
}


def log_access(func):
    """
    Decorador que registra el acceso de un usuario a un endpoint en la base de datos.
    Este decorador registra la hora de acceso del usuario, el endpoint al que se accedió,
    el ID de usuario y la fecha de registro del usuario. Los datos se almacenan en una tabla 
    de registros de endpoint en la base de datos.
    """

    @wraps(func)
    def create_log(*args, **kwargs):
        token = get_jwt_identity()
        user_id = token
        endpoint = request.endpoint
        start_time = datetime.now()
        connection = mysql.connector.connect(**connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute(
            'SELECT registerdate FROM users WHERE id = %s', (user_id,))
        register_date = mycursor.fetchone()
        new_log = "INSERT INTO endpointlogs (useriID, endpoint, startTime, register_date) " \
            "VALUES (%s, %s, %s, %s)"
        add = (user_id, endpoint, start_time, register_date[0])
        mycursor.execute(new_log, add)
        connection.commit()
        connection.close()
        return func(*args, **kwargs)
    return create_log


@app.route('/')
def welcome():
    """
    Renderiza la plantilla HTML "welcome.html" y la devuelve como respuesta HTTP.
    La plantilla HTML "welcome.html" contiene un mensaje de bienvenida.
    Este endpoint se utiliza como página de inicio de la aplicación web.
    """
    return render_template('welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Maneja el registro de un nuevo usuario mediante una solicitud POST 
    que contiene un nombre de usuario y una contraseña. Verifica si 
    el nombre de usuario ya está en uso, si es así devuelve un mensaje de error.
    Si el nombre de usuario no está en uso, guarda la información del usuario 
    en la base de datos y redirige a la página de inicio de sesión.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw'].encode('utf-8')
        connection = mysql.connector.connect(**connectionDatabase)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user:
            connection.close()
            return jsonify({'mensaje': 'El usuario ya existe'}), 400
        password_hash = hashlib.sha256(password).hexdigest()
        register_date = datetime.now()
        sql = "INSERT INTO users (username, password, register_date) VALUES (%s, %s, %s)"
        add = (username, password_hash, register_date)
        cursor.execute(sql, add)
        connection.commit()
        connection.close()
        return redirect(url_for('login', json=request.form), code=307)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Maneja la autenticación de un usuario a través de credenciales
    de inicio de sesión proporcionadas a través de una solicitud POST.
    Si las credenciales son válidas, se crea un token de acceso para 
    el usuario y se registra una nueva sesión en la base de datos. 
    Si las credenciales son inválidas, se devuelve un mensaje de error.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw'].encode('utf-8')
        connection = mysql.connector.connect(**connectionDatabase)
        mycursor = connection.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        add = (username,)
        mycursor.execute(sql, add)
        user = mycursor.fetchone()

        if user is None or hashlib.sha256(password).hexdigest() != user[2]:
            connection.close()
            return jsonify({"msg": "Credenciales inválidas"}), 401

        token = create_access_token(identity=user[0])
        time = datetime.now()
        expire = time + timedelta(minutes=10)
        user_agent = request.headers.get('User-Agent')
        user_agent_parsed = parse(user_agent)
        user_browser = user_agent_parsed.browser.family
        new_session = "INSERT INTO sessions (userID, token, browser, os, createdAt, " \
            "expiresAt) VALUES (%s, %s, %s,%s,%s,%s)"
        add = (user[0], token, user_browser,
               platform.system(), time, expire)
        mycursor.execute(new_session, add)
        connection.commit()
        connection.close()

        return jsonify({
            "AccessToken": token,
            "UserID": user[0],
            "Browser": user_browser,
            "OperativeSystem": platform.system(),
            "CreatedAt": time.strftime('%Y-%m-%d %H:%M:%S'),
            "ExpiredAt": expire.strftime('%Y-%m-%d %H:%M:%S')
        }), 200
    return render_template('login.html')


@app.route('/ligamx/jugadores')
@jwt_required()
@log_access
def get_jugadores():
    """ 
    Obtiene la lista de todos los jugadores de la Liga MX y 
    devuelve la lista en formato JSON. 
    """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM players")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/equipos')
def get_equipos():
    """ 
    Obtiene la lista de todos los equipos de la Liga MX y 
    devuelve la lista en formato JSON. 
    """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teams")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/goleadores')
def get_goleadores():
    """ 
    Obtiene la lista de los 10 mejores goleadores de la Liga MX 
    y devuelve la lista en formato JSON. 
    """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, lastName, team, goals FROM players "
                   "ORDER BY goals DESC LIMIT 10")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/asistidores')
def get_asistidores():
    """ 
    Obtiene la lista de los 10 mejores asistidores de la Liga MX 
    y devuelve la lista en formato JSON. 
    """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, lastName, team, assists FROM players ORDER BY assists DESC LIMIT 10")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/campeonatos')
def get_campeonatos():
    """ 
    Obtiene la lista de los equipos de la Liga MX ordenados 
    por su cantidad de campeonatos y devuelve la lista en formato JSON.
    """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, trophies FROM teams ORDER BY trophies DESC")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/jugadores/valorMercado')
def get_valor_mercado():
    """ Obtiene la lista de todos los jugadores de la Liga MX ordenados 
    por su valor de transferencia y devuelve la lista en formato JSON. """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, lastName, team, transferPrice FROM players ORDER BY transferPrice DESC")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/jugadores/mexicanos')
def get_mexicanos():
    """ 
    Obtiene la lista de todos los jugadores mexicanos de la Liga MX
    y devuelve la lista en formato JSON. 
    """
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, lastName, team, position FROM players WHERE nationality='México'")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route("/bye")
def adios():
    """
    Manda un mensaje en formato JSON con una despedida.
    """
    return jsonify(despedida="bye bye")


@app.route("/about")
def about():
    """ 
    Abre el archivo de liga.json devolviendo una lista de los endpoints de la Liga MX.
    """
    with open("liga.json", encoding='utf-8') as archivo:
        datos = json.load(archivo)
    return datos


if __name__ == '__main__':
    app.run(debug=True)
