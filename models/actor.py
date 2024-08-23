from init import db, ma

class Actor(db.Model):
    __tablename__ = "actors"
    id_actor = db.Column(db.Integer, primary_key=True)
    actor_first_name = db.Column(db.String(100), nullable=False)
    actor_last_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    dob = db.Column(db.Date)


class ActorSchema(ma.Schema):
    class Meta:
        fields = ("id_actor", "actor_first_name",
                  "actor_last_name", "country", "dob")
        

actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)