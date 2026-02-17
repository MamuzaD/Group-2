"""
Counter API Implementation
"""

from flask import Flask, jsonify
from . import status

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return duplicate_counter_response(name)
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

def duplicate_counter_response(name):
    """Duplicate counter error response"""
    return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT


@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return duplicate_counter_response(name)
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["GET"])
def nonexistent_counter(name):
    if not counter_exists(name):
        return jsonify(
            {"error": f"Counter {name} is nonexistent"}
        ), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['GET'])
def retrieve_existing_counter(name):
    """Retrieve an existing counter"""
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} does not exist"}), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} not found"}), status.HTTP_404_NOT_FOUND
    COUNTERS.pop(name)
    return jsonify({name: name}), status.HTTP_204_NO_CONTENT
  
@app.errorhandler(405)
def http_method_not_allowed(error):
    """Custom handler for invalid HTTP methods"""
    return jsonify({"error": "Method Not Allowed"}), status.HTTP_405_METHOD_NOT_ALLOWED
