from flask import Blueprint, request, jsonify
from models.actor import Actor, actors_schema
from init import db
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authoriseAsAdmn


actor_command = Blueprint("actor", __name__, url_prefix = "/actors")

# ADD NEW ACTOR FROM THE BODY OF THE HTTP REQUEST
@actor_command.route("/", methods=["POST"])
# with this decorator if a user wants to access this route needs to be autenticated with a jwt token
@jwt_required()
def add_actors():
    new_actors = []
    body = request.get_json()
    for i in body:
        actor = Actor(
            actor_first_name=i["actor_first_name"],
            actor_last_name=i.get("actor_last_name"),
            country=i.get("country"),
            dob=i.get("dob")
        )
        new_actors.append(actor)

        # add to session
        db.session.add_all(new_actors)
        db.session.commit()
    return {"message": "New data actors added!"}


@actor_command.route("/", methods=["GET"])
def get_actors():
    # query
    statement = db.select(Actor)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(actors_schema.dump(results))


# DELETE records from actors
@actor_command.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_actor(id):
    if not authoriseAsAdmn():
        return {"authorization error":"you are not authorized"},403
    else:
        statement = db.select(Actor).filter_by(id_actor=id)
        result = db.session.scalar(statement)

        if result:
            db.session.delete(result)
            db.session.commit()
            return {"delete":f"actor with id: {id} deleted"}
        else:
            return {"error":f"the actor with id: {id} doesn not exist!"}