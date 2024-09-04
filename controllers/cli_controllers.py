from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.movie import Movie
from models.actor import Actor
from models.director import Director
from models.review import Review
from datetime import date

# we need to create the Blueprint for each decorator and then register in the main.py
db_commands = Blueprint("db", __name__)

# CLI COMMANDS AREA
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created succesfully")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped succesfully")


# ADD NEW ACTORS AND MOVIES DIRECTLY FROM THE CODE USING THE COMMAND "flask seed"


@db_commands.cli.command("seed")
def seed_database():
    # When seeding the database, make sure you’re inserting the actors into the actors table before inserting movies into the movies table.
    # This ensures that you have valid actor_id values to associate with each movie. And then wensure actors are saved before adding movies (db.session.commit())

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
        actor_first_name="Hugh",
        actor_last_name="Jackman",
        country="Australia",
        dob="1979-01-17")

    actor_four = Actor()
    actor_four.actor_first_name = "Keanu"
    actor_four.actor_last_name = "Reeves"
    actor_four.country = "America"
    actor_four.dob = "1986-12-05"

    actors = [actor_one, actor_two, actor_three, actor_four]
    #add to the session
    db.session.add_all(actors)

    print("Actors data entered correctly!")

    directors = [
        Director(
            director_first_name = "Tim",
            director_last_name = "Burton",
            country = "America",
        ),
        Director(
            director_first_name = "James",
            director_last_name = "Cameron",
            country = "America",
        ),
            Director(
            director_first_name = "Carlo",
            director_last_name = "Vanzina",
            country = "Italy",
        )
    ]

    db.session.add_all(directors)

    print("Directors added succesfully!")


    movie_one = Movie()
    movie_two = Movie()
    movie_three = Movie()
    movie_four = Movie()

    movie_one.title = "Matrix"
    movie_one.length = "180"
    movie_one.release_date = "1999-02-12"
    movie_one.genre = "Sci-Fi"
    # adding actor by retrieving it
    statement = db.select(Actor).filter_by(actor_first_name = "Keanu", actor_last_name = "Reeves")
    actor = db.session.scalar(statement)
    movie_one.actor=actor

    # adding director
    statement = db.select(Director).filter_by(id_director=2)
    director = db.session.scalar(statement)
    movie_one.director=director
   

    movie_two.title = "Swordfish code"
    movie_two.length = "120"
    movie_two.release_date = "2004-02-12"
    movie_two.genre = "Action"
    statement = db.select(Actor).filter_by(actor_first_name="Hugh", actor_last_name="Jackman")
    actor = db.session.scalar(statement)
    movie_two.actor_id = actor.id_actor

    # adding director
    statement = db.select(Director).filter_by(id_director=2)
    director = db.session.scalar(statement)
    movie_two.director=director

    movie_three.title = "Pirate of the Caribbean"
    movie_three.length = "180"
    movie_three.release_date = "2004-02-12"
    movie_three.genre = "Fantasy/Adventure"
    statement = db.select(Actor).filter_by(actor_first_name="Johnny", actor_last_name="Deep")
    actor = db.session.scalar(statement)
    movie_three.actor_id = actor.id_actor

    # adding director
    statement = db.select(Director).filter_by(id_director=1)
    director = db.session.scalar(statement)
    movie_three.director=director

    movie_four.title = "Iron Man"
    movie_four.length = "120"
    movie_four.release_date = "2008-04-21"
    movie_four.genre = "Fantasy/Adventure"
    statement = db.select(Actor).filter_by(actor_first_name="Tony", actor_last_name="Stark")
    actor = db.session.scalar(statement)
    movie_four.actor_id = actor.id_actor

    # adding director
    statement = db.select(Director).filter_by(id_director=3)
    director = db.session.scalar(statement)
    movie_four.director=director


    # adding to session
    movies = [movie_one, movie_two, movie_three, movie_four]
    db.session.add_all(movies)

    print("Movies data entered correctly!")


    users = [
        User(
            name="User 1",
            email="cao@gmail.com",
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



    reviews = [
        
    Review(
        message = "The movie was awesome!",
        date = date.today(),
        user = users[0],
        movies = movies[0]
    ),

    Review(
        message = "worst actor ever!",
        date = date.today(),
        user = users[1],
        movies = movies[1]
    ), 

    Review(
        message = "I'd would watch it again",
        date = date.today(),
        user = users[0],
        movies = movies[1]
    ) 
    ]
    print("Reviews added!")

    db.session.add_all(reviews)
   
   # commit to the session
    db.session.commit()
