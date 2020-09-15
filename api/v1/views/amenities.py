#!/usr/bin/python3
"""
Module for methods used by app_view blueprint
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.amenity import Amenity
from flasgger import swag_from


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_spec/get_amenities.yml')
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenity_list = list(storage.all(Amenity).values())
    amenity_dict = [amenity.to_dict() for amenity in amenity_list]
    return jsonify(amenity_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_spec/get_amenity.yml')
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_spec/create_amenity.yml')
def create_amenity():
    """Creates a new Amenity object"""
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_obj = Amenity()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_obj, key, value)
    new_obj.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('swagger_spec/delete_amenity.yml')
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('swagger_spec/update_amenity.yml')
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict())
