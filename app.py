from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

app = Flask(__name__)
# DB CONNECTION AREA
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://tomato:123456@localhost:5432/ripe_tomato"
# CREATE THE ECNRYPTING KEY
app.config["JWT_SECRET_KEY"] = "secret"

ma = Marshmallow(app)
db = SQLAlchemy(app)
# CREATE OBJECTS FOR ENCRYPTING PASSWORD
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ADD A USER MODEL


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)

# CREATE MODEL of actor table


class Actor(db.Model):
    __tablename__ = "actors"
    id_actor = db.Column(db.Integer, primary_key=True)
    actor_first_name = db.Column(db.String(100), nullable=False)
    actor_last_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    dob = db.Column(db.Date)


class Movie(db.Model):
    __tablename__ = "movies"
    id_movie = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    length = db.Column(db.String(100))
    release_date = db.Column(db.Date)

# CREATE SCHEMA MARSHMALLOW


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "admin")


class ActorSchema(ma.Schema):
    class Meta:
        fields = ("id_actor", "actor_first_name",
                  "actor_last_name", "country", "dob")


class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id_movie", "title", "genre", "length", "release_date")


# CREATE INSTANCE OF MARSHMALLOW SCHEMA
# when we create a schema for the user we have to exclude the passwrd because
# they dont need to be converted into a Python readable format
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)

# CLI COMMANDS AREA


@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created succesfully")


@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped succesfully")

# ADD NEW ACTORS AND MOVIES DIRECTLY FROM THE CODE USING THE COMMAND "flask seed"


@app.cli.command("seed")
def seed_database():
    add_actor()
    add_movie()
    add_users()
    # commit to the session
    db.session.commit()


def add_actor():
    actor_one = Actor(
        actor_first_name="Tony",
        actor_last_name="Stark",
        country="America",
        dob="1975-06-11")

    actor_two = Actor(
        actor_first_name="Johnny",
        actor_last_name="Deep",
        country="America",
        dob="1967-11-08")

    actor_three = Actor(
        actor_first_name="Christian",
        actor_last_name="De sica",
        country="Italy",
        dob="1979-01-17")

    actor_four = Actor()
    actor_four.actor_first_name = "Claudia"
    actor_four.actor_last_name = "Gerini"
    actor_four.country = "Italy"
    actor_four.dob = "1986-12-05"

    actors = [actor_one, actor_two, actor_three, actor_four]
    db.session.add_all(actors)
    print("Actors data entered correctly!")


def add_movie():
    movie_one = Movie()
    movie_two = Movie()
    movie_three = Movie()

    movie_one.title = "Matrix"
    movie_one.length = "180"
    movie_one.release_date = "1999-02-12"

    movie_two.title = "Swordfish code"
    movie_two.length = "120"
    movie_two.release_date = "2004-02-12"

    movie_three.title = "Pirate of the Caribbean"
    movie_three.length = "180"
    movie_three.release_date = "2004-02-12"

    # adding to session
    movies = [movie_one, movie_two, movie_three]
    db.session.add_all(movies)
    print("Movies data entered correctly!")


def add_users():
    users = [
        User(
            name="User 1",
            email="ciao@gmail.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8'),
            admin=True
        ),

        User(
            name="User 2",
            email="alberto@gmail.com",
            password=bcrypt.generate_password_hash("5678").decode('utf8'),
            admin=True
        ),

        User(
            name="User 3",
            email="marco@gmail.com",
            password=bcrypt.generate_password_hash("10998765").decode('utf8')
        )
    ]
    db.session.add_all(users)
    print("Users added succesfully!")

# ROUTING AREA


@app.route("/")
def hello():
    return "Welcome to Ripe Tomatoes API"

# ADD NEW ACTOR FROM THE BODY OF THE HTTP REQUEST


@app.route("/actors", methods=["POST"])
# with this decorator if a user wants to access this route needs to be autenticated with a jwt token
@jwt_required()
def add_actors():
    new_actors = []
    body = request.get_json()
    for i in body:
        actor = Actor(
            actor_first_name=i["actor_first_name"],
            actor_last_name=i.get("actor_last_name"),
            country=i.get("country"),
            dob=i.get("dob")
        )
        new_actors.append(actor)

        # add to session
        db.session.add_all(new_actors)
        db.session.commit()
    return {"message": "New data actors added!"}


@app.route("/actors", methods=["GET"])
def get_actors():
    # query
    statement = db.select(Actor)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(actors_schema.dump(results))


@app.route("/movies", methods=["GET"])
def get_movies():
    # query
    statement = db.select(Movie)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(movies_schema.dump(results))

# GET ALL THE USERS
@app.route("/users", methods=["GET"])
def get_users():
    statement = db.select(User)
    results = db.session.scalars(statement)

    data = users_schema.dump(results)
    return jsonify(data)

# REGISTER USER


@app.route("/auth/register", methods=["POST"])
def register_user():
    try:
        # Body of the request
        body_data = request.get_json()
        # Exctracting the password from the body of the request
        password = body_data["password"]
        # Hashing the password using bcrypt object
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf8')
        # Create a user instance using the User model
        user = User(
            name=body_data["name"],
            email=body_data["email"],
            password=hashed_password,
            admin=body_data["admin"]
        )
        # Add it to the session
        db.session.add(user)
        # Commit
        db.session.commit()
        # Return a message
        return user_schema.dump(user), 201
    except IntegrityError as e:
        return {"error": "Email already exists"}, 400

# LOGIN USER


@app.route("/auth/login", methods=["POST"])
def login_user():
    # Find the uer with that email
    body = request.get_json()

    # If the user exists and the password matches
    # check if the user password is in the database
    statement = db.select(User).filter_by(email=body.get("email"))
    result = db.session.scalar(statement)

    # check if the user exist and the password matches using check_password_hash method that takes two arguments
    # (plain text password from the body request and hashed password from the database) 
    if result and bcrypt.check_password_hash(result.password, body.get("password")):
        # we create an authentication token (jwt) through the module that we imported
        # the arguments are indentity=the id of the statement result converted to string and
        # the expiring session time using timedelta library. (after 1 day the login expires )
        token = create_access_token(identity=str(
            result.id), expires_delta=timedelta(days=1))

        # return the token
        # return {"token": token, "email": result.email, "admin":result.admin }
        return {"token":token, "user":user_schema.dump(result)}
    # else return an error message
    else:
        return {"error":"Invalid email or password"},401
    
# DELETE records from movies
@app.route("/movies/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_movie(id):
    if not authoriseAsAdmn():
        return {"authorization error":"you are not authorized"},403
    else:
        statement = db.select(Movie).filter_by(id_movie=id)
        result = db.session.scalar(statement)

        if result:
            db.session.delete(result)
            db.session.commit()
            return {"delete":f"movie with id: {id} deleted"}
        else:
            return {"error":f"the movie with id: {id} doesn not exist!"}
        
# DELETE records from actors
@app.route("/actors/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_actor(id):
    if not authoriseAsAdmn():
        return {"authorization error":"you are not authorized"},403
    else:
        statement = db.select(Actor).filter_by(id_actor=id)
        result = db.session.scalar(statement)

        if result:
            db.session.delete(result)
            db.session.commit()
            return {"delete":f"actor with id: {id} deleted"}
        else:
            return {"error":f"the actor with id: {id} doesn not exist!"}


def authoriseAsAdmn():
    # we receive the token and we look which user ID the token is linked to
    # get the id of the user from the jwt token using get_jwt_identity() function
    user_id = get_jwt_identity()
    #find the user in the db with the id
    statement = db.select(User).filter_by(id=user_id)
    result = db.session.scalar(statement)
    # check if the user is admin or not 
    admin = result.admin
    # return True if the admin is True of False if the admin is False
    if admin:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(debug=True)
