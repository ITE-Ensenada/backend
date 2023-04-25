from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, create_access_token
from datetime import datetime, timedelta
from user_agents import parse
from functools import wraps
import platform
import hashlib
import mysql.connector
import json

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


def log_access(f):
    @wraps(f)
    def createLog(*args, **kwargs):
        token = get_jwt_identity()
        userID = token
        endpoint = request.endpoint
        startTime = datetime.now()
        connection = mysql.connector.connect(**connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute(
            'SELECT registerdate FROM users WHERE id = %s', (userID,))
        registerDate = mycursor.fetchone()
        newLog = "INSERT INTO endpointlogs (useriID, endpoint, startTime, registerDate) VALUES (%s, %s, %s, %s)"
        add = (userID, endpoint, startTime, registerDate[0])
        mycursor.execute(newLog, add)
        connection.commit()
        connection.close()
        return f(*args, **kwargs)
    return createLog


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
        passwordH = hashlib.sha256(password).hexdigest()
        registerDate = datetime.now()
        sql = "INSERT INTO users (username, password, registerDate) VALUES (%s, %s, %s)"
        add = (username, passwordH, registerDate)
        cursor.execute(sql, add)
        connection.commit()
        connection.close()
        return redirect(url_for('login', json=request.form), code=307)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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

        newSession = "INSERT INTO sessions (userID, token, browser, os, createdAt, expiresAt) VALUES (%s, %s, %s,%s,%s,%s)"
        add = (user[0], token, user_browser,
               platform.system(), time, expire)
        mycursor.execute(newSession, add)
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
    connection = mysql.connector.connect(**connectionDatabase)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, name, lastName, team, goals FROM players ORDER BY goals DESC LIMIT 10")
    headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    connection.close()
    json_data = []
    for result in results:
        json_data.append(dict(zip(headers, result)))
    return jsonify(json_data)


@app.route('/ligamx/asistidores')
def get_asistidores():
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
def get_valorMercado():
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
    return jsonify(despedida="bye bye")


@app.route("/about")
def about():
    with open("liga.json") as archivo:
        datos = json.load(archivo)
    return datos


if __name__ == '__main__':
    app.run(debug=True)
