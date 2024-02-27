#!/usr/bin/python3
"""a new view for State objects that handles all default RESTFul
API actions """
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = [s.to_dict() for s in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def id_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    """Creates a State"""
    dict = request.get_json(silent=True)
    if dict is None:
        abort(400, 'Not a JSON')
    if dict.get("name") is None:
        abort(400, 'Missing name')
    new_status = State(**dict)
    new_status.save()
    return jsonify(new_status.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    dict = request.get_json(silent=True)
    if dict is None:
        abort(400, 'Not a JSON')
    keys_substract = ['id', 'created_at', 'updated_at']
    for key, val in dict.items():
        if key not in keys_substract:
            setattr(state, key, val)
    storage.save()
    return jsonify(state.to_dict()), 200
