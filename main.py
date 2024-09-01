import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controllers import db_commands
from controllers.auth_controller import auth_command
from controllers.actor_controller import actor_command
from controllers.movie_controller import movie_command
from controllers.director_controller import director_command

def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

# importing the objects to initialize the flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # we need to create the Blueprint for each decorator and then register in the main.py
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_command)
    app.register_blueprint(actor_command)
    app.register_blueprint(movie_command)
    app.register_blueprint(director_command)

    return app