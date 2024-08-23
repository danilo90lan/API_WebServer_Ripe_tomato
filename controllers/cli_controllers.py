from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.movie import Movie
from models.actor import Actor

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
    #add to the session
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