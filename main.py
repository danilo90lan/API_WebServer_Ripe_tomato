import os
from flask import Flask

from init import db, ma, bcrypt, jwt
# from controllers.cli_controllers import db_commands
# from controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")


# importing the objects to initialize the flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app