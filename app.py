import sys

from flask import Flask, jsonify, reqparse
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

parser.add_argument(
    'date',
    type=inputs.date,
    help="Can't find the date or it has the wrong format!",
    required=True
)
parser.add_argument(
    'name',
    type=str,
    help="The name argument is required!",
    required=True
)


class HelloWorldResource(Resource):
    def get(self):
        result = {"data": "There are no events for today!"}
        return jsonify(result)
    

    def post(self):
        args = parser.parse_args()
        return args['name']


api.add_resource(HelloWorldResource, '/event/today')
api.add_resource(HelloWorldResource, '/event/')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
