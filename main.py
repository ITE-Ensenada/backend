#!/usr/bin/python3
import mysql.connector
import json
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid  # for public id
from datetime import datetime, timedelta
from ua_parser import user_agent_parser
from functools import wraps


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'anime'
app.config["SECRET_KEY"] = "EstaEsLaClaveSecreta853245"

mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    """Retorna un template dedicado al inicio de sesion"""
    return render_template("home.html")

# decorator for verifying the JWT


def token_required(variable_f):
    """Funcion encargada de validar si un token es valido"""
    @wraps(variable_f)
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
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            cur = mysql.connection.cursor()

            t_public_id = data['public_id']
            sql = "select * from users where public_id = %s "
            cur.execute(sql, [t_public_id])
            current_user = cur.fetchone()

            if current_user is None:
                return jsonify({
                    'message': 'Token is invalid !!'
                }), 401
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return variable_f(current_user, *args, **kwargs)

    return decorated

# User Database Route
# this route sends back list of users


@app.route('/user', methods=['GET'])
@token_required
def get_all_users():
    """Retorna todos los usuarios registrados en la base"""
    # querying the database
    # for all the entries in it
    cur = mysql.connection.cursor()
    cur.execute(""" select * from users""")
    users_fetch_all = cur.fetchall()
    # converting the query objects
    # to list of jsons

    all_users = []
    for user in users_fetch_all:
        all_users.append({
            "id": user[0],
            "public_id": user[1],
            "name": user[2],
            "email": user[3],
            "password": user[4],

        })
    return jsonify({'users': all_users})


# route for logging user in
@app.route('/login', methods=['POST'])
def login():
    """Funcion para poder hacer un login con email y password"""
    # creates dictionary of form data
    print(request.form.get("email"))
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    cur = mysql.connection.cursor()
    cur.execute("""select * from users where email=%s """,
                (auth.get('email'),))
    user_f = cur.fetchone()

    if not user_f:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    password = user_f[4]

    if check_password_hash(password, auth.get('password')):
        parsed_string = user_agent_parser.Parse(request.user_agent.string)
        user_browser = parsed_string["user_agent"]["family"]
        user_os = parsed_string["os"]["family"]
        entry_time = datetime.utcnow()

        # generates the JWT Token
        token = jwt.encode({
            'public_id': user_f[1],
            'exp': entry_time + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token, "public_id": user_f[1], "user_browser": user_browser, "user_os": user_os, "entry_time": entry_time}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods=['POST'])
def signup():
    """Funcion para hacer un registro con los campos: name, email y password"""
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor()
    query_sql = "SELECT * FROM users WHERE email = %(email)s"

    cur.execute(query_sql,  {'email': "Ricardo@gmail.com"})
    user_f = cur.fetchone()

    if user_f is None:
        # database ORM object
        t_public_id = str(uuid.uuid4())
        t_name = name
        t_mail = email
        t_password = generate_password_hash(password)

        insert_stmt = (
            "INSERT INTO users (public_id, name, email, password) "
            "VALUES (%s, %s, %s, %s)"
        )
        data = (t_public_id, t_name, t_mail, t_password)
        cur = mysql.connection.cursor()
        cur.execute(insert_stmt, data)
        mysql.connection.commit()
        print(user_f)
        return make_response('Successfully registered.', 201)
    return make_response('User already exists. Please Log in.', 202)


@app.route("/anime", methods=['GET'])
@token_required
def search_anime_id():
    """Funcion que regresa todos los animes almacenados en la base"""
    try:
        id_anime = int(request.args["anime-id"])
    except:
        id_anime = False
    if isinstance(id_anime, int):
        cur = mysql.connection.cursor()
        cur.execute("""select A.id_anime as "Id",A.title as "Title",
                    A.description as "Description",A.year as "Year",
        B.name as "Mangaka"
        ,C.season as "Season"
        ,D.name as "Gender"
        ,E.type as "Rated"
        , A.img_cover as "Image"
        from animes A

        inner JOIN authors B 
        on A.author=B.id_author
        
        inner join seasons C
        on A.season = C.id_season
        
        inner join genders D
        on A.gender = D.id_gender
        
        inner join rated E
        ON D.rated = E.id_rated
 
        WHERE A.id_anime = %s""", (id_anime,))
        data_anime = cur.fetchone()
        if data_anime is None:
            return jsonify({"error": "Anime not found"})
        anime = {
            "id": data_anime[0],
            "title": data_anime[1],
            "description": data_anime[2],
            "year": data_anime[3],
            "mangaka": data_anime[4],
            "season": data_anime[5],
            "gender": data_anime[6],
            "rated": data_anime[7],
            "image": data_anime[8],

        }
        return jsonify(anime)
    return jsonify({"error": "An error occurred"})


@app.route("/anime/author/", methods=['GET'])
@token_required
def search_manga_id():
    """Funcion que regresa todos los animes del id de un author dado"""
    try:
        id_author = int(request.args["author-id"])
    except:
        id_author = False
    if isinstance(id_author, int):
        cur = mysql.connection.cursor()
        cur.execute("""select A.id_anime as "Id",A.title as "Title",A.description as 
                    "Description",A.year as "Year",
        B.name as "Mangaka"
        ,C.season as "Season"
        ,D.name as "Gender"
        ,E.type as "Rated"
        , A.img_cover as "Image"
        from animes A

        inner JOIN authors B 
        on A.author=B.id_author
        
        inner join seasons C
        on A.season = C.id_season
        
        inner join genders D
        on A.gender = D.id_gender
        
        inner join rated E
        ON D.rated = E.id_rated
 
        WHERE B.id_author = %s
        
        """, (id_author,))
        data_anime = cur.fetchone()
        if data_anime is None:
            return jsonify({"error": "Anime not found"})
        anime = {
            "id": data_anime[0],
            "title": data_anime[1],
            "description": data_anime[2],
            "year": data_anime[3],
            "mangaka": data_anime[4],
            "season": data_anime[5],
            "gender": data_anime[6],
            "rated": data_anime[7],
            "image": data_anime[8],
        }
        return jsonify(anime)
    return jsonify({"error": "Ocurrió un error"})


@app.route("/search/anime/", methods=['GET'])
@token_required
def search_anime_title():
    """Funcion que regresa todos los animes que coincidan con el titulo dado"""
    title = request.args["title"]
    if len(title) == 0:
        return jsonify({"error": "El titulo no puede estar vacio"})
    title = "%"+title+"%"
    cur = mysql.connection.cursor()
    cur.execute("""select A.id_anime as "Id",A.title as 
                "Title",A.description as "Description",A.year as "Year",
            B.name as "Mangaka"
            ,C.season as "Season"
            ,D.name as "Gender"
            ,E.type as "Rated"
            , A.img_cover as "Image"
            from animes A

            inner JOIN authors B 
            on A.author=B.id_author
            
            inner join seasons C
            on A.season = C.id_season
            
            inner join genders D
            on A.gender = D.id_gender
            
            inner join rated E
            ON D.rated = E.id_rated
 
            WHERE A.title LIKE %s """, (title,))
    all_data = cur.fetchall()
    all_animes = []
    for anime in all_data:
        all_animes.append({
            "id": anime[0],
            "title": anime[1],
            "description": anime[2],
            "year": anime[3],
            "mangaka": anime[4],
            "season": anime[5],
            "gender": anime[6],
            "rated": anime[7],
            "image": anime[8],
        })
    return jsonify(all_animes)


@app.route("/anime/all", methods=["GET"])
@token_required
def all_animes():
    """Funcion que regresa todos los animes almacenados en la api"""
    cur = mysql.connection.cursor()
    cur.execute("""select A.id_anime as "Id",A.title as "Title",A.description as 
                "Description",A.year as "Year",
    B.name as "Mangaka"
    ,C.season as "Season"
    ,D.name as "Gender"
    ,E.type as "Rated"
    , A.img_cover as "Image"
    from animes A

    inner JOIN authors B 
    on A.author=B.id_author
    
    inner join seasons C
    on A.season = C.id_season
    
    inner join genders D
    on A.gender = D.id_gender
    
    inner join rated E
    ON D.rated = E.id_rated
    
    ORDER BY A.id_anime ASC""")
    all_data = cur.fetchall()
    all_animes = []
    for anime in all_data:
        all_animes.append({
            "id": anime[0],
            "title": anime[1],
            "description": anime[2],
            "year": anime[3],
            "mangaka": anime[4],
            "season": anime[5],
            "gender": anime[6],
            "rated": anime[7],
            "image": anime[8],
        })
    return jsonify(all_animes)


@app.route("/author/all/", methods=["GET"])
@token_required
def all_authors():
    """Funcion que regresa todos los autores registrados en la api"""
    cur = mysql.connection.cursor()
    cur.execute("""select * from authors order by authors.id_author asc""")
    all_data = cur.fetchall()
    all_authors = []
    for author in all_data:
        all_authors.append({
            "id_author": author[0],
            "name": author[1],
        })
    return jsonify(all_authors)


@app.route("/about")
def anime():
    """Funcion que muestra informacion sobre como usar la api y endpoins disponibles"""
    with open("aboutl.json", "r") as data:
        return jsonify(json.load(data))


@app.errorhandler(404)
def page_not_found(error):
    """En caso de un error 404, retornar un json con un mensaje de error"""
    error = {
        "Code": 404,
        "Error": "Endpoint not found"
    }
    return jsonify(error)


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True)
