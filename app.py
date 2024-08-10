from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
## DB CONNECTION AREA
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://tomato:123456@localhost:5432/ripe_tomato"

ma = Marshmallow(app)
db = SQLAlchemy(app)



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
class ActorSchema(ma.Schema):
   class Meta:
      fields = ("id_actor", "actor_first_name", "actor_last_name", "country", "dob")

class MovieSchema(ma.Schema):
  class Meta:
    fields = ("id_movie", "title", "genre", "length", "release_date")
   

# CREATE INSTANCE OF MARSHMALLOW SCHEMA
movie_schema = MovieSchema()
movie_schema = MovieSchema(many=True)
actor_schema = ActorSchema()
actor_schema = ActorSchema(many=True)

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
  #commit to the session
  db.session.commit()

def add_actor():
  actor_one = Actor(
    actor_first_name = "Tony",
    actor_last_name = "Stark",
    country = "America",
    dob = "1975-06-11")
  
  actor_two = Actor(
    actor_first_name = "Johnny",
    actor_last_name = "Deep",
    country = "America",
    dob = "1967-11-08")
  
  actor_three = Actor(
    actor_first_name = "Christian",
    actor_last_name = "De sica",
    country = "Italy",
    dob = "1979-01-17")
  
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

# ROUTING AREA
@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

# ADD NEW ACTOR FROM THE BODY OF THE HTTP REQUEST
@app.route("/actors", methods=["POST"])
def add_actors():
  new_actors = []
  body = request.get_json()
  for i in body:
    actor = Actor(
      actor_first_name = i["actor_first_name"],
      actor_last_name = i.get("actor_last_name"),
      country = i.get("country"),
      dob = i.get("dob")
    )
    new_actors.append(actor)

    # add to session
    db.session.add_all(new_actors)
    db.session.commit()
  return {"message":"New data actors added!"}

@app.route("/actors", methods=["GET"])
def get_actors():
  #query
  statement = db.select(Actor)
  #exeution of the query
  results = db.session.scalars(statement)

  # now we need to convert the results nto json readeble format using marshmallow schema
  return jsonify(actor_schema.dump(results))

@app.route("/movies", methods=["GET"])
def get_movies():
  #query
  statement = db.select(Movie)
  #exeution of the query
  results = db.session.scalars(statement)

  # now we need to convert the results nto json readeble format using marshmallow schema
  return jsonify(movie_schema.dump(results))

if __name__ == "__main__":
  app.run(debug=True)