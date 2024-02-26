#!/usr/bin/python3
"""a script to return the status of the API"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app, origins=['0.0.0.0'])
app.register_blueprint(app_views)


@app.teardown_appcontext
def session_close(exception):
    """close session"""
    storage.close()


@app.errorhandler(404)
def handle_404(exep):
    """error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """not importing module if it was imported"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
