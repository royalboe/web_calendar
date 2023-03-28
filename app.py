import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
db = SQLAlchemy(app)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

# initialize the app with the extension
# db.init_app(app)

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


class EventSchema(Schema):
    id = fields.Integer()
    event = fields.String()
    date = fields.DateTime(dt_format='iso8601')


class TodayEvent(Resource):
    def get(self):
        schema = EventSchema(many=True)
        events = Event.query.filter(Event.date == datetime.date.today()).all()
        if events:
            return schema.dump(events)

        result = {"data": "There are no events for today!"}
        return schema.dump(result)


class PostEvent(Resource):
    def post(self):
        # schema = EventSchema()
        args = parser.parse_args()
        result = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": datetime.datetime.strftime(args['date'], "%Y-%m-%d")
        }
        db.session.add(Event(date=args['date'].date(), event=args['event']))
        db.session.commit()
        # return schema.dump(args)
        return result, 200


class GetAllEvent(Resource):
    def get(self):
        schema = EventSchema(many=True)
        events = Event.query.all()
        if events:
            return schema.dump(events)
        result = {"data": "There are no events!"}
        return schema.dump(result)


api.add_resource(TodayEvent, '/event/today')
api.add_resource(PostEvent, '/event')
api.add_resource(GetAllEvent, '/event')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
