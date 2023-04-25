from flask import Flask, request, jsonify, render_template, url_for, redirect
import jwt
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import mysql.connector

#import jwt
from flask_jwt_extended import JWTManager

app = Flask(__name__)


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "paradysesecret"  # Change this!
jwt = JWTManager(app)


#Database connection
cnxBD = mysql.connector.connect(
    host="localhost",
    user = "root", 
    password ="admin@paradyse08",
    database="GraphicsCards",
    port="3306",
)

@app.route('/test_db_connection')
def test_db_connection():
    cur = cnxBD.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    result = cur.fetchone()[0]
    return f"Number of records in users: {result}"

def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    ).decode('UTF-8')
    
    # Store token in database
    cursor = cnxBD.cursor()
    cursor.execute('INSERT INTO user_tokens (user_id, token) VALUES (%s, %s)', (user_id, token))
    cnxBD.commit()

    return token
    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['sub']
            cursor = cnxBD.cursor()
            cursor.execute('SELECT * FROM user_tokens WHERE user_id = %s AND token = %s', (current_user, token))
            user_token = cursor.fetchone()
            if not user_token:
                raise Exception()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



#ROUTES

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = cnxBD.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'Invalid credentials'}), 401

        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            user['salt'].encode('utf-8'),
            100000
        )

        if hashed_password != user['password']:
            return jsonify({'message': 'Invalid credentials'}), 401

        token = generate_token(user['id'])

        return redirect(url_for('protected'), code=307)

    return render_template('auth/login.html')


@app.route('/protected')
@token_required
def protected(current_user):
    return jsonify({'message': f'This is a protected route, {current_user}!'})





if __name__ == "__main__":
    app.run(debug=True)