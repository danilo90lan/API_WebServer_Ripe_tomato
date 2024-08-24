from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authoriseAsAdmn
from init import db
from models.movie import Movie, movies_schema

movie_command = Blueprint("movie", __name__, url_prefix = "/movies")

@movie_command.route("/", methods=["GET"])
def get_movies():
    # query
    statement = db.select(Movie)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(movies_schema.dump(results))


    
# DELETE records from movies
@movie_command.route("/<int:id>", methods=["DELETE"])
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