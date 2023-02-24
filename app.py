import sys

from flask import Flask, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWorldResource(Resource):
    def get(self):
        result = {"data": "There are no events for today!"}
        return jsonify(result)


api.add_resource(HelloWorldResource, '/event/today')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
