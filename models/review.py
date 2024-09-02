from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__="reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id= db.Column(db.Integer, db.ForeignKey("movies.id_movie"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    movies = db.relationship("Movie", back_populates="reviews")

class ReviewSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name","email"])
    movies = fields.Nested("MovieSchema", only=["id_movie","title"])
   
    class Meta:
        fields = ("review_id", "message", "date", "user", "movies", "comments")

comment_schema = ReviewSchema()
comments_schema = ReviewSchema(many=True)