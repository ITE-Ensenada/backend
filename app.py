# python3 -m venv venv
# source virtual/bin/active
# flask --app app run -h ip


from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import json
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Eso_Tilin'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./AllMusic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistic_name = db.Column(db.String(50))
    nationality = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)


class Artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistic_name = db.Column(db.String(50))
    nationality = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(10), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)


class Songs(db.Model):
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


with app.app_context():
    db.create_all()


def token_required(f):
    @wraps(f)
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
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
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
    return "<h1 style= text-align: center;>All Music</h1>"


@app.route("/login", methods=['POST'])
def login():
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
    else:
        return make_response('User already exists. Please Log in.', 202)


@app.route("/author")
@token_required
def get_authors(current_user):
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
def get_artists(current_user):
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
def get_songs(current_user):
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
    f = open('allmusic.json')
    data = json.load(f)
    f.close()
    return data


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': "Page not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)
