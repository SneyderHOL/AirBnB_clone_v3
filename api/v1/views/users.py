#!/usr/bin/python3
"""
Module for methods used by app_view blueprint
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User
import hashlib


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    user_list = list(storage.all(User).values())
    user_dict = [user.to_dict() for user in user_list]
    return jsonify(user_dict)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves an User object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a new User object"""
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_obj = User()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_obj, key, value)
    new_obj.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes an User object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates an User object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(user_obj, key, value)
        if key == 'password':
            pw = value
            encoding = 'utf-8'
            pw_hashed = hashlib.md5(pw.encode(encoding)).hexdigest()
            setattr(user_obj, key, pw_hashed)

    user_obj.save()
    return jsonify(user_obj.to_dict())
