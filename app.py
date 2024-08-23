



# ROUTING AREA


@app.route("/")
def hello():
    return "Welcome to Ripe Tomatoes API"

# ADD NEW ACTOR FROM THE BODY OF THE HTTP REQUEST


@app.route("/actors", methods=["POST"])
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


@app.route("/actors", methods=["GET"])
def get_actors():
    # query
    statement = db.select(Actor)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(actors_schema.dump(results))


@app.route("/movies", methods=["GET"])
def get_movies():
    # query
    statement = db.select(Movie)
    # exeution of the query
    results = db.session.scalars(statement)

    # now we need to convert the results nto json readeble format using marshmallow schema
    return jsonify(movies_schema.dump(results))

# GET ALL THE USERS
@app.route("/users", methods=["GET"])
def get_users():
    statement = db.select(User)
    results = db.session.scalars(statement)

    data = users_schema.dump(results)
    return jsonify(data)



    
# DELETE records from movies
@app.route("/movies/<int:id>", methods=["DELETE"])
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
        
# DELETE records from actors
@app.route("/actors/<int:id>", methods=["DELETE"])
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


def authoriseAsAdmn():
    # we receive the token and we look which user ID the token is linked to
    # get the id of the user from the jwt token using get_jwt_identity() function
    user_id = get_jwt_identity()
    #find the user in the db with the id
    statement = db.select(User).filter_by(id=user_id)
    result = db.session.scalar(statement)
    # check if the user is admin or not 
    admin = result.admin
    # return True if the admin is True of False if the admin is False
    if admin:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(debug=True)
    