
# Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
from datetime import datetime

from conexionBD import *  # Importando conexion BD
from funciones import *  # Importando mis Funciones
from routes import *  # Vistas

import re
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/dashboard', methods=['GET', 'POST'])
def loginUser():
    conexion_MySQLdb = connectionBD()
    if 'conectado' in session:
        return render_template('public/dashboard/home.html', dataLogin=dataLoginSesion())
    else:
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = str(request.form['email'])
            password = str(request.form['password'])

            # Comprobando si existe una cuenta
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM login_python WHERE email = %s", [email])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['password'], password):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                    session['conectado'] = True
                    session['id'] = account['id']
                    session['tipo_user'] = account['tipo_user']
                    session['nombre'] = account['nombre']
                    session['apellido'] = account['apellido']
                    session['email'] = account['email']
                    msg = "Ha iniciado sesión correctamente."
                    return render_template('public/dashboard/home.html', dataLogin=dataLoginSesion())
                else:
                    msg = 'Datos incorrectos, por favor verfique!'
                    return render_template('public/modulo_login/index.html')
            else:
                return render_template('public/modulo_login/index.html')
    return render_template('public/modulo_login/index.html',)


# Registrando una cuenta de Usuario
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registerUser():
    msg = ''
    conexion_MySQLdb = connectionBD()
    if request.method == 'POST':
        tipo_user = 2
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        repite_password = request.form['repite_password']
        # current_time = datetime.datetime.now()

        # Comprobando si ya existe la cuenta de Usuario con respecto al email
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM login_python WHERE email = %s', (email,))
        account = cursor.fetchone()
        cursor.close()  # cerrrando conexion SQL

        if account:
            msg = 'Ya existe el Email!'
        elif password != repite_password:
            msg = 'Disculpa, las clave no coinciden!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Disculpa, formato de Email incorrecto!'
        elif not email or not password or not password or not repite_password:
            msg = 'El formulario no debe estar vacio!'
        else:
            # La cuenta no existe y los datos del formulario son válidos,
            password_encriptada = generate_password_hash(
                password, method='sha256')
            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute('INSERT INTO login_python (tipo_user, nombre, apellido, email, password) VALUES (%s, %s, %s, %s, %s)',
                           (tipo_user, nombre, apellido, email, password_encriptada))
            conexion_MySQLdb.commit()
            cursor.close()
            msg = 'Cuenta creada correctamente!'

        return render_template('public/modulo_login/index.html')
    return render_template('public/layout.html', dataLogin=dataLoginSesion())


@app.route('/actualizar-mi-perfil/<id>', methods=['POST'])
def actualizarMiPerfil(id):
    if 'conectado' in session:
        msg = ''
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            sexo = request.form['sexo']
            pais = request.form['pais']

            if (request.form['password']):
                password = request.form['password']
                repite_password = request.form['repite_password']

                if password != repite_password:
                    msg = 'Las claves no coinciden'
                    return render_template('public/dashboard/home.html', dataLogin=dataLoginSesion())
                else:
                    nueva_password = generate_password_hash(
                        password, method='sha256')
                    conexion_MySQLdb = connectionBD()
                    cur = conexion_MySQLdb.cursor()
                    cur.execute("""
                        UPDATE login_python 
                        SET 
                            nombre = %s, 
                            apellido = %s, 
                            email = %s, 
                            password = %s
                        WHERE id = %s""", (nombre, apellido, email, nueva_password, id))
                    conexion_MySQLdb.commit()
                    cur.close()  # Cerrando conexion SQL
                    conexion_MySQLdb.close()  # cerrando conexion de la BD
                    msg = 'Perfil actualizado correctamente'
                    return render_template('public/dashboard/home.html', dataLogin=dataLoginSesion())
            else:
                msg = 'Perfil actualizado con exito'
                conexion_MySQLdb = connectionBD()
                cur = conexion_MySQLdb.cursor()
                cur.execute("""
                    UPDATE login_python 
                    SET 
                        nombre = %s, 
                        apellido = %s, 
                        email = %s
                    WHERE id = %s""", (nombre, apellido, email, id))
                conexion_MySQLdb.commit()
                cur.close()
                return render_template('public/dashboard/home.html', dataLogin=dataLoginSesion())
        return render_template('public/dashboard/home.html', dataLogin=dataLoginSesion())


if __name__ == "__main__":
    app.run(debug=True, port=8000)
