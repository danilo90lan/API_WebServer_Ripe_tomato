from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

db = SQLAlchemy()
ma = Marshmallow()
# CREATE OBJECTS FOR ENCRYPTING PASSWORD
bcrypt = Bcrypt()
jwt = JWTManager()