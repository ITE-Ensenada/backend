# python3 -m venv venv
# source virtual/bin/active
# flask --app app run -h ip

"""Importaciones generales para el proyecto"""
import uuid
import json
from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Eso_Tilin'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./AllMusic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    """Modelo para los usuarios registrados"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Authors(db.Model):
    """Modelo para los autores de las canciones"""
    id = db.Column(db.Integer, primary_key=True)
    artistic_name = db.Column(db.String(50))
    nationality = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)


class Artists(db.Model):
    """Modelo para los artistas de las canciones"""
    id = db.Column(db.Integer, primary_key=True)
    artistic_name = db.Column(db.String(50))
    nationality = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)


class Songs(db.Model):
    """Modelo para las canciones"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    duration = db.Column(db.Integer(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    record_company = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    album = db.Column(db.String(50), nullable=False)
    format = db.Column(db.String(10), nullable=False)
    licenses = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'),
                          nullable=False)


# with app.app_context():
#     db.create_all()


def token_required(func):
    """Función para validación de tokens"""
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token not found.'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Users.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except:
            return jsonify({
                'message': 'Invalid token.'
            }), 401
        return func(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users():
    """Endpoint para obtener todos los usuarios registrados"""
    users = Users.query.all()
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'name': user.name,
            'email': user.email
        })

    return jsonify({'users': output})


@app.route("/")
def main():
    """Endpoint para endpoint principal"""
    return "<h1 style= text-align: center;>All Music</h1>"


@app.route("/login", methods=['POST'])
def login():
    """Endpoint para generar un token de inicio de sesión"""
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required."'}
        )

    user = Users.query.filter_by(email=auth.get('email')).first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist."'}
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password."'}
    )


@app.route('/signup', methods=['POST'])
def signup():
    """Endpoint para registrar un usuario"""
    data = request.form

    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first()
    if not user:
        user = Users(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)

    return make_response('User already exists. Please Log in.', 202)


@app.route("/author")
@token_required
def get_authors():
    """Endpoint para obtener todos los autores"""
    authors = Authors.query.all()
    output = []
    for author in authors:
        output.append({
            'artistic_name': author.artistic_name,
            'nationality': author.nationality,
            'birthday': author.birthday,
            'real_name': author.real_name
        })
    return jsonify({'authors': output})


@app.route("/artist")
@token_required
def get_artists():
    """Endpoint para obtener todos los artistas"""
    artists = Artists.query.all()
    output = []
    for artist in artists:
        output.append({
            'artistic_name': artist.artistic_name,
            'nationality': artist.nationality,
            'birthday': artist.birthday,
            'real_name': artist.real_name
        })
    return jsonify({'artists': output})


@app.route("/song")
@token_required
def get_songs():
    """Endpoint para obtener todas las canciones"""
    songs = Songs.query.all()
    output = []
    for song in songs:
        output.append({
            'name': song.name,
            'genre': song.genre,
            'duration': song.duration,
            'year': song.year,
            'record_company': song.record_company,
            'language': song.language,
            'album': song.album,
            'format': song.format,
            'licenses': song.licenses,
            'author_id': song.author_id,
            'artist_id': song.artist_id
        })
    return jsonify({'songs': output})


@app.route("/about")
def about():
    """Endpoint para obtener la información del proyecto"""
    with open('allmusic.json', encoding="utf-8") as file:
        data = json.load(file)
    return data


@app.errorhandler(404)
def page_not_found():
    """Manejador de errores de ruta"""
    return jsonify({'error': "Page not found."}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
