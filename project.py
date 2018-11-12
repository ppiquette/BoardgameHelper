from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from database_setup import User, HeroRealmEvent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boardgamehelper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
session = db.session


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class HeroRealmEventSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'description', 'user1_id', 'user2_id')


event_schema = HeroRealmEventSchema()
events_schema = HeroRealmEventSchema(many=True)


#######################################################################################################################
# User endpoints
#

# GET user information
@app.route("/user", methods=["GET"])
@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id=None):
    if user_id:
        user = session.query(User).filter(User.id == user_id).one()
        return user_schema.jsonify(user)
    else:
        all_users = session.query(User)
        return users_schema.jsonify(all_users)


# POST new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username=username, email=email)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


#######################################################################################################################
# Event endpoints
#

# GET event information
@app.route("/event", methods=["GET"])
@app.route("/event/<event_id>", methods=["GET"])
def event_detail(event_id=None):
    if event_id:
        event = session.query(HeroRealmEvent).filter(HeroRealmEvent.id == event_id).one()
        return event_schema.jsonify(event)
    else:
        all_events = session.query(HeroRealmEvent)
        return events_schema.jsonify(all_events)


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

