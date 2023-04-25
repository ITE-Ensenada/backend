#python3 -m venv .env => crea una virtualizacion
#source .env/bin/activate => entra dentro de la virtualizacion
#deactivate => desactiva la virtualizacion
#pip install Flask => instala flask
#flask --app hello ru => metodo para correr la aplicacion desde flaske

from flask import Flask, jsonify, render_template, url_for
import json

import mysql.connector

cnx = mysql.connector.connect(
    user = "root", 
    password ="admin@paradyse08",
    host="localhost",
    database="GraphicsCards",
    port="3306",
)

app = Flask(__name__)

@app.route("/")
def main():
    return render_template(url_for('auth/login.html'))

@app.route('/test_db_connection')
def test_db_connection():
    cur = cnx.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    result = cur.fetchone()[0]
    return f"Number of records in users: {result}"

@app.route("/index")
def index():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users")
    for (id_user, username, password) in cursor:
        print("{} - {} {} ({})".format(id_user, username, password))
    data = cursor.fetchall()
    return jsonify(data)

if __name__=='__main__':
    app.run()