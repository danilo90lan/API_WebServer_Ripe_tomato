from init import db, ma
from marshmallow import fields

class Director(db.Model):
    __tablename__ = "directors"
    id_director = db.Column(db.Integer, primary_key=True)
    director_first_name = db.Column(db.String(100), nullable=False)
    director_last_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))

    # adding the constraint cascade="all, delete" to the actor relationship
    movies = db.relationship("Movie", back_populates="director", cascade="all, delete")

class DirectorSchema(ma.Schema):
    movies = fields.List(fields.Nested("MovieSchema", only=["title"]))
    class Meta:
        fields = ("id_director", "director_first_name",
                  "director_last_name", "country", "movies")
        
        ordered=True

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)