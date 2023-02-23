from flask import Flask
from flask_restful import Api, Resource
import sys

app = Flask(__name__)
api = Api(app)

class HelloWorldResource(Resource):
    def get(self):
        return {
            "message": "Hello from the REST API!"
            }

api.add_resource(HelloWorldResource, '/hello')


# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
