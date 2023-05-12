#Created by tparadyse
#April, 2023

"""
General imports for working in API
"""
from functools import wraps
from datetime import datetime, timedelta
import uuid # for public id
from flask import Flask, request, jsonify, make_response, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt # imports for PyJWT authentication

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'tparadyseinbackend'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GraphicsCards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)

# Database ORMs
# pylint: disable=R0903
class User(db.Model):
    """
    Class to generate and create a user table
    """
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))

# Tables ORMs for Graphics Cards Endpoints
# pylint: disable=R0903
class GraphicCard(db.Model):
    """
    Class to generate and create a graphics_cards table
    """
    id = db.Column(db.Integer, primary_key = True)
    technologic_id = db.Column(db.Integer, unique = True)
    brand_id = db.Column(db.Integer, unique = True)
    model_id = db.Column(db.Integer, unique = True)

# pylint: disable=R0903
class Technologic(db.Model):
    """
    Class to generate and create a technologic table
    """
    id = db.Column(db.Integer, primary_key = True)
    technologic_id = db.Column(db.String(50), unique = True)
    name_technology = db.Column(db.Integer)
    founding_year = db.Column(db.String(80))
    founders_name = db.Column(db.String(80))
    origin_country = db.Column(db.String(80))
    main_branch = db.Column(db.String(80))

# pylint: disable=R0903
class Brand(db.Model):
    """
    Class to generate and create a brand table
    """
    id = db.Column(db.Integer, primary_key = True)
    brand_id = db.Column(db.String(50), unique = True)
    brand_name = db.Column(db.String(100))
    origin_region = db.Column(db.String(80))
    brand_creator = db.Column(db.String(80))
    store_distributors = db.Column(db.String(80))
    performance_level = db.Column(db.String(80))
    compatibility_level = db.Column(db.String(80))
    range_prices = db.Column(db.String(80))
    range_reputation = db.Column(db.String(80))

# pylint: disable=R0903
class Model(db.Model):
    """
    Class to generate and create a model table
    """
    id = db.Column(db.Integer, primary_key = True)
    model_id = db.Column(db.String(50), unique = True)
    model_name = db.Column(db.String(80))
    model_number = db.Column(db.String(80), unique = True)
    generation_series = db.Column(db.Integer)
    time_base = db.Column(db.Integer)
    boost_gpu = db.Column(db.Integer)
    memory_vdedicate = db.Column(db.Integer)
    memory_vtype = db.Column(db.String(80))
    vmemory_bandwidth = db.Column(db.String(80))
    number_cores = db.Column(db.Integer)
    frecuancy_cores = db.Column(db.Integer)
    number_cores = db.Column(db.String(80))
    physical_size = db.Column(db.String(80))
    cooler_dimension = db.Column(db.String(80))
    required_conector = db.Column(db.String(80))
    power_supply = db.Column(db.String(80))
    model_price = db.Column(db.Integer)
    unique_features = db.Column(db.String(80))

# pylint: disable=R0903
class Logs(db.Model):
    """
    Class to generate and create a logs table
    """
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, unique = True)
    endpoint = db.Column(db.String(80))
    register_date = db.Column(db.String(80))
    session_date = db.Column(db.String(80))

# pylint: disable=R0903
class Session(db.Model):
    """
    Class to generate and create a session table
    """
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, unique = True)
    session_date = db.Column(db.String(80))
    divice = db.Column(db.String(50))
    operative_system = db.Column(db.String(80))

#with app.app_context():
    #db.create_all()

# decorator for verifying the JWT
def token_required(func):
    """
    Function to create a validate token to be used before 
    to start a endpoint page to authenticate
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            print(token)
            print(app.config['SECRET_KEY'])
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

            current_user = User.query\
				.filter_by(user_id = data['user_id'])\
				.first()
        except jwt.exceptions.DecodeError:
            return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users context to the routes
        return func(current_user, *args, **kwargs)

    return decorated

# User Database Route
# this route sends back list of users
@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
    """
    Function to get all user of User table
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
			'user_id': user.user_id,
			'name' : user.name,
			'email' : user.email
		})

    return jsonify({'users': output})

# route for logging user in
@app.route('/login', methods =['GET', 'POST'])
def login():
    """
    Function to login before to start navigate
    """
    # returns a login.html template
    if request.method == 'GET':
        return render_template('auth/login.html')

    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'user_id': user.user_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], "HS256")
        return make_response(jsonify({'token' : token}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods =['GET','POST'])
def signup():
    """
    Function to signup or create a user account
    """
    if request.method == 'GET':
        return render_template('auth/signup.html')
	# creates a dictionary of the form data
    data = request.form

	# gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

	# checking for existing user
    user = User.query\
		.filter_by(email = email)\
		.first()
    if not user:
		# database ORM object
        user = User(
			user_id = str(uuid.uuid4()),
			name = name,
			email = email,
			password = generate_password_hash(password)
		)
		# insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)

	# returns 202 if user already exists
    return make_response('User already exists. Please Log in.', 202)


# Endpoints for Graphics Cards API

# this route sends back list of all graphics cards
@app.route('/graphics-cards', methods =['GET'])
@token_required
def get_all_graphics_cards(current_user):
    """
    Function to get all graphics cards from graphics_cards table
    """
    graphic = GraphicCard.query.all()
    output = []
    for graphic_card in graphic:
        output.append({
			'technologic_id': graphic_card.technologic_id,
			'brand_id' : graphic_card.brand_id,
			'model_id' : graphic_card.model_id
		})

    return jsonify({'graphic': output})

# this route sends back list of especific graphics cards{}
@app.route('/graphics-cards{model_id}', methods =['GET'])
@token_required
def get_graphic_card_model(current_user):
    """
    Function to get an specific graphic card from model table
    """
    graphic = Model.query.all()
    output = []
    for graphic_card in graphic:
        output.append({
			'model_name': graphic_card.model_name,
			'model_number' : graphic_card.model_number,
			'generation_series' : graphic_card.generation_series,
            'memomy_vdedicate' : graphic_card.memory_vdedicate,
            'memory_vtype' : graphic_card.memory_vtype
		})

    return jsonify({'graphic': output})

@app.route('/')
def index():
    """
    This function redirect the / route to /login route
    """
    return redirect(url_for('login'))

if __name__ == "__main__":
	# setting debug to True enables hot reload
	# and also provides a debugger shell
	# if you hit an error while running the server
    app.run(host='0.0.0.0', port=5009)
 
