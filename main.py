"""Este programa es una API que consulta datos generales de videojuegos"""
from datetime import datetime, timedelta
from functools import wraps
import uuid  # for public id
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'VGDB_riskorain'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
    """Clase que accede a la tabla User en la database"""
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))

class Videogames(db.Model):
    """Clase que accede a la tabla Videogames en la database"""
    id = db.Column(db.Integer, primary_key=True)
    videogame_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    developer = db.Column(db.String(70))
    publisher = db.Column(db.String(80))
    release_year = db.Column(db.Integer)

class Developers(db.Model):
    """Clase que accede a la Developers Videogames en la database"""
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    latest_game = db.Column(db.String(70))
    ceo_name = db.Column(db.String(80))
    fundation_year = db.Column(db.Integer)

class Publishers(db.Model):
    """Clase que accede a la tabla Publishers en la database"""
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    most_succesfull_game = db.Column(db.String(70))
    ceo_name = db.Column(db.String(80))
    fundation_year = db.Column(db.Integer)

#with app.app_context():
#    db.create_all()
# decorator for verifying the JWT

def token_required(f):
    """
    Esta funcion es la que verificara si
    se requiere token o no para acceder al endpoint 
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            print(token)
            print(app.config['SECRET_KEY'])
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])

            current_user = User.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/')
def index():
    return "<h1><center>VGDb</center></h1>"

# User Database Route
# this route sends back list of users

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    Aqui toma la data del usuario, para poder
    crear el token enseguida segun los datos de este
    """
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'public_id': user.public_id,
            'name': user.name,
            'email': user.email
        })

    return jsonify({'users': output})

# route for logging user in

@app.route('/login', methods=['POST'])
def login():
    """
    Este es el login de nuestro API
    """
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query\
        .filter_by(email=auth.get('email'))\
        .first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'], "HS256")
        return make_response(jsonify({'token': token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

# signup route

@app.route('/signup', methods=['POST'])
def signup():
    """
    La funcion de ingreso al API
    """
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.query\
        .filter_by(email=email)\
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
########################################################################

@app.route('/videogames', methods=['GET'])
@token_required
def videogames(current_user):
    """
    La funcion obtendra y mostrara todos los datos
    del videojuego
    """
    games = Videogames.query.all()
    output = []
    for game in games:
        output.append({
            'videogame_id': game.videogame_id,
            'name': game.name,
            'developer': game.developer,
            'publisher': game.publisher,
            'release_year': game.release_year,
        })
    return jsonify({'consulta': output})

@app.route('/developers', methods=['GET'])
@token_required
def developers(current_user):
    """
    Esta funcion obtendra y mostrara la data de
    los developers
    """
    developers = Developers.query.all()
    output = []
    for developer in developers:
        output.append({
            'developer_id': developer.developer_id,
            'name': developer.name,
            'latest_game': developer.latest_game,
            'ceo_name': developer.ceo_name,
            'fundation_year': developer.fundation_year,
        })
    return jsonify({'consulta': output})

@app.route('/publishers', methods=['GET'])
@token_required
def publishers(current_user):
    """
    Esta funcion mostrra todo sobre los publishers
    """
    publishers = Publishers.query.all()
    output = []
    for publisher in publishers:
        output.append({
            'publisher_id': publisher.publisher_id,
            'name': publisher.name,
            'most_succesfull_game': publisher.most_succesfull_game,
            'ceo_name': publisher.ceo_name,
            'fundation_year': publisher.fundation_year,
        })
    return jsonify({'consulta': output})

    ################################################################
if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True)
