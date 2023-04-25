# Flask
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

# JWT
import jwt

# SQLITE3
import sqlite3

# Otros
from  werkzeug.security import generate_password_hash, check_password_hash
import uuid
import json
from datetime import datetime, timedelta
from functools import wraps
from user_agents import parse


# Objeto de Flask
app = Flask(__name__)
# SECRET KEY
app.config['SECRET_KEY'] = 'BeethovenWeed'
# COnfiguracion de la base de datos con SQLalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cannalite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_public = db.Column(db.String(50), unique = True)
    user_name = db.Column(db.String(100))
    user_email = db.Column(db.String(70), unique = True)
    user_password = db.Column(db.String(80))
    user_registerdate = db.Column(db.String(80))

class Log(db.Model):
    log_id = db.Column(db.Integer, primary_key = True)
    log_email = db.Column(db.String(70))
    log_date = db.Column(db.String(80))

class Strain(db.Model):
    strain_id = db.Column(db.Integer, primary_key=True)
    strain_name = db.Column(db.String(255))
    strain_type = db.Column(db.String(255))
    strain_year = db.Column(db.Integer)
    strain_thc = db.Column(db.Float)
    strain_cbd = db.Column(db.Float)
    strain_description = db.Column(db.Text)
    strain_effects = db.Column(db.Text)
    strain_flavors = db.Column(db.Text)

class Creator(db.Model):
    creators_name = db.Column(db.String(255))
    creators_country = db.Column(db.String(255))
    creators_mail = db.Column(db.String(255))
    creators_phone = db.Column(db.String(255))
    creators_license = db.Column(db.String(255), primary_key= True)
    creators_strain = db.Column(db.String(255))
    creators_lab = db.Column(db.String(255))

class Dispensary(db.Model):
    dispensary_name = db.Column(db.String(255))
    dispensary_state = db.Column(db.String(255))
    dispensary_city = db.Column(db.String(255))
    dispensary_address = db.Column(db.String(255))
    dispensary_phone = db.Column(db.String(255))
    dispensary_mail = db.Column(db.String(255), primary_key = True)

class Award(db.Model):
    awards_id = db.Column(db.Integer, primary_key=True)
    awards_name = db.Column(db.String(255))
    awards_date = db.Column(db.Date)
    awards_entity = db.Column(db.String(255))
    awards_winner = db.Column(db.String(255))

class Concentrate(db.Model):
    concentrate_id = db.Column(db.Integer, primary_key=True)
    concentrate_name = db.Column(db.String(255))
    concentrate_strain = db.Column(db.String(255))
    concentrate_thc = db.Column(db.Float)
    concentrate_cbd = db.Column(db.Float)
    concentrate_dose = db.Column(db.String(255))
    concentrate_type = db.Column(db.String(255))
    concentrate_effects = db.Column(db.Text)
    concentrate_flavors = db.Column(db.Text)
    concentrate_description = db.Column(db.Text)


# with app.app_context():
#     db.create_all()

# Funcion para obtener los datos del usuario
def get_user_info():
    user_agent = request.headers.get('User-Agent')
    user_agent_parsed = parse(user_agent)
    user_os = user_agent_parsed.os.family
    user_browser = user_agent_parsed.browser.family
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    current_time = datetime.now()
    entry_time = current_time.strftime(time_format)
    return {
        'entry_time': entry_time,
        'browser': user_browser,
        'os': user_os
    }

# Verificardor del JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # El jwt se obtiene del header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # Return 401 si no hay token en el header
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            # decode del payload
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(user_public = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # return del usuario
        return  f(current_user, *args, **kwargs)
    return decorated


@app.route("/")
def main():
        return "<center><h1>CANNAPI CHAD API DEPLOY</h1></center><marquee>ADRIAN Y TONY</marquee>"

# Login
@app.route('/login', methods=['POST'])
def login():

    # Obtiene la info del usuario del request
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    user = User.query.filter_by(user_email = auth.get('email')).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.user_password, auth.get('password')):
        user_info = get_user_info()
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(minutes=10)),
            'user_os': user_info['os'],
            'user_browser': user_info['browser']
        },
            app.config['SECRET_KEY'])
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

#Register
@app.route('/register', methods = ['POST'])
def register():
    data = request.form
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
    user = User.query.filter_by(user_email = email).first()
    if not user:
        user = User(
            user_public = str(uuid.uuid4()),
            user_name = name,
            user_email = email,
            user_password = generate_password_hash(password),
            user_registerdate = datetime.now()
        )
        log = Log(
            log_email = email,
            log_date = datetime.now())
        # insert user
        db.session.add(user)
        db.session.add(log)
        db.session.commit()
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)

#Autheticated
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified'

@app.route("/about")
def about():
    f = open('cannapi.json')
    display = json.load(f)
    return jsonify(display)


@app.route("/bye")
def bye():
    return "<h1> Recuerden fumar bandita</h1>"

@app.route('/api', methods=['GET'])
@token_required
def get_data():
    strains = Strain.query.all()
    creators = Creator.query.all()
    dispensaries = Dispensary.query.all()
    awards = Award.query.all()
    concentrates = Concentrate.query.all()
    data = {
        'strains': [strain.__dict__ for strain in strains],
        'creators': [creator.__dict__ for creator in creators],
        'dispensaries': [dispensary.__dict__ for dispensary in dispensaries],
        'awards': [award.__dict__ for award in awards],
        'concentrates': [concentrate.__dict__ for concentrate in concentrates]
    }
    return jsonify(data)

@app.route("/awards", methods =['GET'])
# @token_required
def awards():
    awards = Award.query.all()
    data = {
       'awards': [award.__dict__ for award in awards]
    }
    return jsonify(data)

@app.route("/concentrate", methods=['GET'])
@token_required
def concentrate():
    concentrates = Concentrate.query,all()
    data = {
        'concentrates': [concentrate.__dict__ for concentrate in concentrates]
    }
    return jsonify(data)

@app.route("/creators", methods=['GET'])
@token_required
def creators():
    creators =  Creator.query.all()
    data = {
        'creators': [creator.__dict__ for creator in creators],
    }
    return jsonify(data)

@app.route("/dispensary", methods=['GET'])
@token_required
def dispensary():
    dispensaries = Dispensary.query.all()
    data = {
        'dispensaries': [dispensary.__dict__ for dispensary in dispensaries]
    }
    return jsonify(data)

@app.route("/strain", methods=['GET'])
@token_required
def strain():
    strains = Strain.query.all()
    data = {
        'strains': [strain.__dict__ for strain in strains]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)
