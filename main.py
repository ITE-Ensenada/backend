#!/usr/bin/python3
import mysql.connector
import json
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session, jsonify,make_response
from flask_mysqldb import MySQL
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid # for public id
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

formData = {}

@app.route("/", methods=['GET', 'POST'])
def home():
    """Retorna un template dedicado al inicio de sesion"""
    return render_template("home.html")

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
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            cur = mysql.connection.cursor()

            tPublicId = data['public_id']
            sql="select * from users where public_id = %s ";
            cur.execute(sql,[tPublicId])
            currentUser = cur.fetchone()
            
            if currentUser is None:
                return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(currentUser, *args, **kwargs)
  
    return decorated
    
# User Database Route
# this route sends back list of users
@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
    """Retorna todos los usuarios registrados en la base"""
    # querying the database
    # for all the entries in it
    cur = mysql.connection.cursor()
    cur.execute(""" select * from users""")
    usersFetchAll = cur.fetchall()
    # converting the query objects
    # to list of jsons

    allUsers = []
    for user in usersFetchAll:
        allUsers.append({
            "id": user[0],
            "public_id": user[1],
            "name": user[2],
            "email": user[3],
            "password": user[4],

        })
    return jsonify({'users': allUsers})


# route for logging user in
@app.route('/login', methods =['POST'])
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
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    
    cur = mysql.connection.cursor()
    cur.execute("""select * from users where email=%s """, (auth.get('email'),))
    userF = cur.fetchone()
  
    if not userF:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
    
    password = userF[4]

    if check_password_hash(password, auth.get('password')):
        parsed_string = user_agent_parser.Parse(request.user_agent.string)
        user_browser = parsed_string["user_agent"]["family"]
        user_os = parsed_string["os"]["family"]
        entry_time = datetime.utcnow()

        # generates the JWT Token
        token = jwt.encode({
            'public_id': userF[1],
            'exp' : entry_time + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token,"public_id": userF[1], "user_browser": user_browser, "user_os":user_os,"entry_time": entry_time }), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )


# signup route
@app.route('/signup', methods =['POST'])
def signup():
    """Funcion para hacer un registro con los campos: name, email y password"""
    # creates a dictionary of the form data
    data = request.form
  
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor()
    querySql = "SELECT * FROM users WHERE email = %(email)s"

    cur.execute(querySql,  { 'email': "Ricardo@gmail.com" })
    userF = cur.fetchone()

    if  userF==None:
        # database ORM object
        tPublicId = str(uuid.uuid4());
        tName = name
        tEmail = email
        tPassword = generate_password_hash(password)

        print(tPassword)

        insert_stmt = (
        "INSERT INTO users (public_id, name, email, password) "
        "VALUES (%s, %s, %s, %s)"
        )
        data = (tPublicId, tName, tEmail, tPassword)
        cur = mysql.connection.cursor()
        cur.execute(insert_stmt, data)
        mysql.connection.commit()
        print(userF);
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


@app.route("/anime", methods=['GET'])
@token_required
def searchAnimeId(current_user):
    """Funcion que regresa todos los animes almacenados en la base"""
    try:
        idAnime = int(request.args["anime-id"])
    except:
        idAnime = False
    if isinstance(idAnime, int):
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
 
        WHERE A.id_anime = %s""", (idAnime,))
        dataAnime = cur.fetchone()
        if dataAnime is None:
            return jsonify({"error": "Anime not found"})
        anime = {
            "id": dataAnime[0],
            "title": dataAnime[1],
            "description": dataAnime[2],
            "year": dataAnime[3],
            "mangaka": dataAnime[4],
            "season": dataAnime[5],
            "gender": dataAnime[6],
            "rated": dataAnime[7],
            "image": dataAnime[8],

        }
        return jsonify(anime)
    else:
        return jsonify({"error": "An error occurred"})


@app.route("/anime/author/", methods=['GET'])
@token_required
def searchMangakaId(current_user):
    """Funcion que regresa todos los animes del id de un author dado"""
    try:
        idAuthor = int(request.args["author-id"])
    except:
        idAuthor = False
    if isinstance(idAuthor, int):
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
        
        """, (idAuthor,))
        dataAnime = cur.fetchone()
        if dataAnime is None:
            return jsonify({"error": "Anime not found"})
        anime = {
            "id": dataAnime[0],
            "title": dataAnime[1],
            "description": dataAnime[2],
            "year": dataAnime[3],
            "mangaka": dataAnime[4],
            "season": dataAnime[5],
            "gender": dataAnime[6],
            "rated": dataAnime[7],
            "image": dataAnime[8],
        }
        return jsonify(anime)
    else:
        return jsonify({"error": "Ocurrió un error"})


@app.route("/search/anime/", methods=['GET'])
@token_required
def searchAnimeTitle(current_user):
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
    allData = cur.fetchall()
    allAnimes = []
    for anime in allData:
        allAnimes.append({
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
    return jsonify(allAnimes)


@app.route("/anime/all", methods=["GET"])
@token_required
def allAnimes(current_user):
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
    allData = cur.fetchall()
    allAnimes = []
    for anime in allData:
        allAnimes.append({
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
    return jsonify(allAnimes)


@app.route("/author/all/", methods=["GET"])
@token_required
def allAuthors(current_user):
    """Funcion que regresa todos los autores registrados en la api"""
    cur = mysql.connection.cursor()
    cur.execute("""select * from authors order by authors.id_author asc""")
    allData = cur.fetchall()
    allAuthors = []
    for author in allData:
        allAuthors.append({
            "id_author": author[0],
            "name": author[1],
        })
    return jsonify(allAuthors)


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
    app.run(debug = True)