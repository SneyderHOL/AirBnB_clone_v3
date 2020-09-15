#!/usr/bin/python3
'''
Starts the Flask web application
'''
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger, swag_from
from models import storage
from api.v1.views import app_views
from os import environ
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")
app.config['SWAGGER'] = {
    'title': 'HBNB API',
    'description': 'RESTFul API for HBNB'
}
swag = Swagger(app)


@app.teardown_appcontext
def teardown_storage(exception):
    """Closes storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    """Runs the app"""
    if environ.get('HBNB_API_HOST'):
        host = environ.get('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if environ.get('HBNB_API_PORT'):
        port = environ.get('HBNB_API_PORT')
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
