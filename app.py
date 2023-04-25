from flask import Flask, request, jsonify, make_response, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

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
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))

# Tables ORMs for Graphics Cards Endpoints
class Graphic_Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    technologic_id = db.Column(db.Integer, unique = True)
    brand_id = db.Column(db.Integer, unique = True)
    model_id = db.Column(db.Integer, unique = True)

class Technologic(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    technologic_id = db.Column(db.String(50), unique = True)
    name_technology = db.Column(db.Integer)
    founding_year = db.Column(db.String(80))
    founders_name = db.Column(db.String(80))
    origin_country = db.Column(db.String(80))
    main_branch = db.Column(db.String(80))

class Brand(db.Model):
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

class Model(db.Model):
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

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, unique = True)
    endpoint = db.Column(db.String(80))
    register_date = db.Column(db.String(80))
    session_date = db.Column(db.String(80))

class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, unique = True)
    session_date = db.Column(db.String(80))
    divice = db.Column(db.String(50))
    operative_system = db.Column(db.String(80))

#with app.app_context():
#  db.create_all()

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
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
        except:
            return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated

# User Database Route
# this route sends back list of users
@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
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
@app.route('/signup', methods =['POST'])
def signup():

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
    else:
		# returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


# Endpoints for Graphics Cards API

# this route sends back list of all graphics cards
@app.route('/graphics-cards', methods =['GET'])
@token_required
def get_all_graphics_cards(current_user):
    graphic = Graphic_Card.query.all()
    output = []
    for gc in graphic:
        output.append({
			'technologic_id': gc.technologic_id,
			'brand_id' : gc.brand_id,
			'model_id' : gc.model_id
		})

    return jsonify({'graphic': output})

# this route sends back list of especific graphics cards{}
@app.route('/graphics-cards{model_id}', methods =['GET'])
@token_required
def get_graphic_card_model(current_user):
    graphic = Model.query.all()
    output = []
    for gc in graphic:
        output.append({
			'model_name': gc.model_name,
			'model_number' : gc.model_number,
			'generation_series' : gc.generation_series,
            'memomy_vdedicate' : gc.memory_vdedicate,
            'memory_vtype' : gc.memory_vtype
		})

    return jsonify({'graphic': output})

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == "__main__":
	# setting debug to True enables hot reload
	# and also provides a debugger shell
	# if you hit an error while running the server
	app.run(debug = True)