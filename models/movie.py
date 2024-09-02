from init import db, ma
from marshmallow import fields

class Movie(db.Model):
    __tablename__ = "movies"
    id_movie = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    length = db.Column(db.String(100))
    release_date = db.Column(db.Date)

    # foreign key (table_name && id name variable)
    # if we use the relationship below created, we dont need to use this field
    actor_id = db.Column(db.Integer, db.ForeignKey("actors.id_actor"), nullable = False)

    director_id = db.Column(db.Integer, db.ForeignKey("directors.id_director"), nullable = False)

    # if we want to fetch more information from the Foreign key other than ID only, 
    # we define a relationship between the two models
    # First parameter is the MODEL NAME (Class name) of the other table, and second parameter (backpopulate) 
    # is the variable defined in actor.py "movies = db.relationship("Movie", back_populates="actor", cascade="all, delete")"
    # that we want to get from the other "side" (Actor table). It's a two ways retrieving
    actor = db.relationship("Actor", back_populates="movies")
    director = db.relationship("Director", back_populates="movies")
    reviews = db.relationship("Review", back_populates="movies", cascade="all, delete")

class MovieSchema(ma.Schema):
    # we need to "unpack" the value of the user in order to be deserialized from marshmallow.
    # it's not a column vale so it cannot be recognize from marshmallow but since we already have the schema 
    # to unpack the value, we used it ("UserSchema") from the User model
    actor = fields.Nested("ActorSchema", only=["id_actor", "actor_first_name", "actor_last_name"])
    director = fields.Nested("DirectorSchema", only=["director_first_name", "director_last_name"])
    reviews = fields.List(fields.Nested("ReviewSchema", exclude=["movies"]))
    
    class Meta:
        fields = ("id_movie", "title", "genre", "length", "release_date", "actor", "director", "reviews")
        ordered=True

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)