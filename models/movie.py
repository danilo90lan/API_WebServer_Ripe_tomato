from init import db, ma

class Movie(db.Model):
    __tablename__ = "movies"
    id_movie = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100))
    length = db.Column(db.String(100))
    release_date = db.Column(db.Date)

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id_movie", "title", "genre", "length", "release_date")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)