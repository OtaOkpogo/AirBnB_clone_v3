#!/usr/bin/python3
"""State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_all():
    """ get all by id """
    all_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_method_state(state_id):
    """ get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def del_method(state_id):
    """ delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def create_obj():
    """ create new instance """
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    
    obj = State(**data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def update_method(state_id):
    """ update method """
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict())

