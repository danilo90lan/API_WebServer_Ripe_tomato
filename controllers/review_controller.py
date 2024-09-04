from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authoriseAsAdmn
from init import db

from flask_jwt_extended import get_jwt_identity

from models.review import Review, review_schema, reviews_schema
from models.movie import Movie

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:movie_id>/reviews")

@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(movie_id):
    # get the comment message from the request body
    body_data = request.get_json()
    # fetch the card with id=card_id
    stmt = db.select(Movie).filter_by(id_movie=movie_id)
    movie_retrieved = db.session.scalar(stmt)
    # if card exists
    if movie_retrieved:
        # create an instance of the comment model
        review = Review (
            message = body_data.get("review"),
            date = date.today(),
            movies = movie_retrieved,
            user_id = get_jwt_identity()
        )
        # add and commit the session
        db.session.add(review)
        db.session.commit()
        # return acknowledgement
        return review_schema.dump(review), 201
    # else
    else:
        # return error
        return {"error": f"Card with id {movie_id} not found."}, 404

@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()  
def delete_review(movie_id, review_id):
    statement = db.select(Review).filter_by(review_id=review_id)
    review = db.session.scalar(statement)
    # if exist
    if review:
        db.session.delete(review)
        db.session.commit()

        return {"message":f"Review {review.message} deleted succesfully"}
    else:
        return {"error":f"Commenty with id {review_id} not found"}, 404