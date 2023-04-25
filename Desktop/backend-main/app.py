# flask imports
from flask import Flask, request, render_template, jsonify, make_response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)


@app.route("/")
def main():
    return "<center><h1>HOLA  ITE ensenada</h1></center><marquee>PAKO</marquee>"

# ENDPOINT


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # obtiene los datos del formulario
        auth = request.form

        if not auth or not auth.get('username') or not auth.get('password'):
            # devuelve 401 si falta algún correo electrónico o contraseña
            return make_response(
                'Could not verify', 401, {
                    'WWW-Authenticate': 'Basic realm="Login required!"'}
            )

        user = user.query.filter_by(username=auth.get('username')).first()

        if not user:
            # devuelve 401 si el usuario no existe
            return make_response(
                'Could not verify', 401, {
                    'WWW-Authenticate': 'Basic realm="Login required!"'}
            )

        if check_password_hash(user.password, auth.get('password')):
            # genera el token de autenticación JWT
            token = jwt.encode(
                {
                    'public_id': user.public_id,
                    'exp': datetime.utcnow() + timedelta(hours=1)  # tiempo de expiración del token
                },
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        # devuelve la respuesta con el token en el encabezado
            return jsonify({'token': token})

        # devuelve 401 si la contraseña es incorrecta
        return make_response(
            'Could not verify', 401, {
                'WWW-Authenticate': 'Basic realm="Login required!"'}
        )
    # renderiza el formulario de inicio de sesión
    return render_template('login.html')
git 

@app.route("/register")
def registro():
    return jsonify(saludo="Asi no se usa el bye tio joderrr")


@app.route("/saludo")
def saludo():
    return '{"value":"bye bye"}'


if __name__ == '__main__':
    app.run()
# flask --app app run
