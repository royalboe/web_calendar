import sys
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, inputs, request, abort
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

# Event Schema Class
class EventSchema(Schema):
    id = fields.Integer()
    event = fields.String()
    date = fields.DateTime(dt_format='iso8601')


class TodayEvent(Resource):
    def get(self):
        schema = EventSchema(many=True)
        events = Event.query.filter(Event.date == datetime.date.today()).all()
        if events is None:
            abort(404, message="There are no events for today!") 
        return schema.dump(events)


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


class DeleteEvent(Resource):
    def delete(self, event_id):
        schema = EventSchema()
        event = Event.query.filter_by(id=event_id).first()
        if event:
            db.session.delete(event)
            db.session.commit()
            result = {"message": "The event has been deleted!"}
            return schema.dump(result)
        abort(404, message="The event doesn't exist!")

class UpdateEvent(Resource):
    def put(self, event_id):
        schema = EventSchema()
        event = Event.query.filter_by(id=event_id).first()
        if event:
            args = parser.parse_args()
            event.event = args['event']
            event.date = args['date']
            db.session.commit()
            result = {"message": "The event has been updated!"}
            return schema.dump(result)
        abort(404, message="The event doesn't exist!")

class GetEvent(Resource):
    def get(self, event_id):
        schema = EventSchema()
        event = Event.query.filter_by(id=event_id).first()
        if event is None:
            abort(404, message="The event doesn't exist!")
        return schema.dump(event)
    
    # def delete(self, event_id):
    #     schema = EventSchema()
    #     event = Event.query.filter_by(id=event_id).first()
    #     if event is None:
    #         abort(404, message="The event doesn't exist!")
    #     db.session.delete(event)
    #     db.session.commit()
    #     result = {"message": "The event has been deleted!"}
    #     return schema.dump(result)
        

class EventMethods(Resource):
    schema = EventSchema()
    def get(self, event_id):
        global schema
        event = Event.query.filter_by(id=event_id).first()
        if event is None:
            abort(404, message="The event doesn't exist!")
        return schema.dump(event)
    
    def delete(self, event_id):
        global schema
        event = Event.query.filter_by(id=event_id).first()
        if event is None:
            abort(404, message="The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        result = {"message": "The event has been deleted!"}
        return jsonify(result)
    
    def put(self, event_id):
        global schema
        event = Event.query.filter_by(id=event_id).first()
        if event is None:
            abort(404, message="The event doesn't exist!")
        args = parser.parse_args()
        event.event = args['event']
        event.date = args['date']
        db.session.commit()
        result = {"message": "The event has been updated!"}
        return jsonify(result)
class GetAllEvent(Resource):
    def get(self):
        schema = EventSchema(many=True)
        start = request.args.get('start_time')
        end = request.args.get('end_time')
        if start and end:
            # start = datetime.datetime.strptime(start, "%Y-%m-%d")
            # end = datetime.datetime.strptime(end, "%Y-%m-%d")
            # events = Event.query.filter(Event.date >= start, Event.date <= end).all()
            events = Event.query.filter(Event.date.between(start, end)).all()
            if events is None:
                abort(404, message="There are no events!")
            return schema.dump(events)
        events = Event.query.all()
        if events is None:
            abort(404, message="There are no events!")
        return schema.dump(events)



api.add_resource(TodayEvent, '/event/today')
api.add_resource(PostEvent, '/event')
api.add_resource(GetAllEvent, '/event')
api.add_resource(EventMethods, '/event/<int:event_id>')
# api.add_resource(DeleteEvent, '/event/<int:event_id>')
# api.add_resource(UpdateEvent, '/event/<int:event_id>')
# api.add_resource(GetEvent, '/event/<int:event_id>')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
