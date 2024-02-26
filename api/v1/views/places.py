#!/usr/bin/python3
""" new view for Place objects that handles all default RESTFul API actions """
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, 'Not a JSON')
    user_id = place_data.get("user_id")
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    name = place_data.get("name")
    if name is None:
        abort(400, 'Missing name')
    place = Place(**place_data)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, 'Not a JSON')
    excluded_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in place_data.items():
        if key not in excluded_keys:
            setattr(place, key, val)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
