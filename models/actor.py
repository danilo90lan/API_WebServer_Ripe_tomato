from init import db, ma
from marshmallow import fields

class Actor(db.Model):
    __tablename__ = "actors"
    id_actor = db.Column(db.Integer, primary_key=True)
    actor_first_name = db.Column(db.String(100), nullable=False)
    actor_last_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    dob = db.Column(db.Date)

    movies = db.relationship("Movie", back_populates="actor")

class ActorSchema(ma.Schema):
    movies = fields.List(fields.Nested("MovieSchema", exclude=["actor"]))
    class Meta:
        #  we include "movies" in the schema that referes to the back_populate value from the other relationship
        #  table and since this is a the one side relationship we cam receive many movies from the other table
        # so we create a list of movie
        fields = ("id_actor", "actor_first_name",
                  "actor_last_name", "country", "dob", "movies")
        
        ordered=True


actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)
