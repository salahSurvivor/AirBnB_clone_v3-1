#!/usr/bin/python3
"""creation of a view of city objs using all the different methods"""
from flask import jsonify, abort, make_response, request
from models.state import State
from api.v1.views import app_views
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ retrieves the list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [city.to_dict() for city in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """ retrieve a City object based on its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletion of a city object"""
    """if If the city_id is not linked to any City object, raise 404"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ creation of a new city using post method"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    content = request.get_json(silent=True)
    if content is None:
        abort(400, 'Not a JSON')
    if content.get("name") is None:
        abort(400, 'Missing name')
    new_city = City(**content)
    new_city.state_id = state.id
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ updating a city using the put method"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json(silent=True) is None:
        abort(400, 'Not a JSON')
    content = request.get_json(silent=True)
    list_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, val in content.items():
        if key not in list_keys:
            setattr(city, key, val)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
