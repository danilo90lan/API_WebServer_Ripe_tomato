from flask import Blueprint, request, jsonify
from models.director import Director, directors_schema
from init import db
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authoriseAsAdmn


director_command = Blueprint("director", __name__, url_prefix = "/directors")

@director_command.route("/", methods=["GET"])
def get_directors():
    # query
    statement = db.select(Director)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(directors_schema.dump(results))

