from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authoriseAsAdmn
from init import db
from models.movie import Movie, movies_schema
from models.actor import Actor
from models.director import Director

movie_command = Blueprint("movie", __name__, url_prefix = "/movies")

@movie_command.route("/", methods=["GET"])
def get_movies():
    # query
    statement = db.select(Movie)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(movies_schema.dump(results))


@movie_command.route("/", methods=["POST"])
@jwt_required()
def add_movie():
    movies = []
    body_request = request.get_json()
    for i in body_request:
        stm = db.select(Actor).filter_by(id_actor=i.get("id_actor"))
        result = db.session.scalar(stm)
        if result:
            movie = Movie (
                title = i.get("title"),
                genre = i.get("genre"),
                length = i.get("length"),
                release_date = i.get("release_date"),
                actor_id = result.id_actor,
                director_id = i.get("director_id")
            )
            movies.append(movie)
        else:
            return {"message":"actor id not found"}
    
    db.session.add_all(movies)
    db.session.commit()
    return jsonify({"message:": "new movies added"})


    
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