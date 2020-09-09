#!/usr/bin/python3
"""
Module for methods used by app_view blueprint with Place class
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects according to a City"""
    city = get_object(City, city_id)
    place_dict = [place.to_dict() for place in city.places]
    return jsonify(place_dict)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place_obj = get_object(Place, place_id)
    return jsonify(place_obj.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_according_to_city(city_id):
    """Creates a new Place object according to a city"""
    data = request.get_json()
    city = get_object(City, city_id)
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = get_object(User, data['user_id'])
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place_obj = Place()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_place_obj, key, value)
    setattr(new_place_obj, 'city_id', city.id)
    new_place_obj.save()
    return make_response(jsonify(new_place_obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = get_object(Place, place_id)
    place_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place_obj = get_object(Place, place_id)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if (key != 'id' and key != 'created_at' and key != 'updated_at' and
                key != 'user_id'):
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict())


def get_object(cls, obj_id):
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj
