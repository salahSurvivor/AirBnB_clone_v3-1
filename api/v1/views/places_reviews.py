#!/usr/bin/python3
"""new view for Review objects that handles all default RESTFul API actions"""
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, 'Not a JSON')
    user_id = review_data.get("user_id")
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    text = review_data.get("text")
    if text is None:
        abort(400, 'Missing text')
    review = Review(**review_data)
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, 'Not a JSON')
    excluded_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, val in review_data.items():
        if key not in excluded_keys:
            setattr(review, key, val)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
