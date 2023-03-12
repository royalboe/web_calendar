import sys
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

# initialize the app with the extension
db.init_app(app)



parser = reqparse.RequestParser()

parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)


class Event(db.Model):
    __tablename__ = 'Event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"{self.date} {self.event}"

    def __str__(self):
        return f"{self.date} {self.event}"
    
with app.app_context():
    db.create_all()

class TodayEvent(Resource):
    def get(self):
        events = Event.query.filter(Event.date == datetime.date.today()).all()
        if events:
            result = {"data": []}
            for event in events:
                result["data"].append({"id": event.id, "event": event.event, "date": datetime.datetime.strftime(event.date,"%Y-%m-%d")})
            return jsonify(result)
        

        result = {"data": "There are no events for today!"}
        return jsonify(result)


class PostEvent(Resource):
    def post(self):
        args = parser.parse_args()
        result = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": datetime.datetime.strftime(args['date'],"%Y-%m-%d")
        }
        db.session.add(Event(date=args['date'].date(), event=args['event']))
        db.session.commit()
        return jsonify(result)


class GetAllEvent(Resource):
    def get(self):
        events = Event.query.all()
        if events:
            result = {"data": []}
            for event in events:
                result["data"].append({"id": event.id, "event": event.event, "date": datetime.datetime.strftime(event.date,"%Y-%m-%d")})
            return jsonify(result)
        result = {"data": "There are no events!"}
        return jsonify(result)


api.add_resource(TodayEvent, '/event/today')
api.add_resource(PostEvent, '/event')
api.add_resource(GetAllEvent, '/event')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)