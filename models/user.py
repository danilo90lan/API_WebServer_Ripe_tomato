from init import db, ma

# ADD A USER MODEL
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "admin")

# CREATE INSTANCE OF MARSHMALLOW SCHEMA
# when we create a schema for the user we have to exclude the passwrd because
# they dont need to be converted into a Python readable format
user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True)
