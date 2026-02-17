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


@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify(
            {"error": f"Counter {name} already exists"}
        ), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["GET"])
def nonexistent_counter(name):
    if not counter_exists(name):
        return jsonify(
            {"error": f"Counter {name} is nonexistent"}
        ), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route("/counters/<name>", methods=["PUT"])
def increment_counter(name):
    # i have purposefully not included a check for if the counter doesn't exist
    # this is because student 6 will need to implement this :)
    COUNTERS[name] += 1
    return jsonify({}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} not found"}), status.HTTP_404_NOT_FOUND
    del COUNTERS[name]
    return jsonify({}), status.HTTP_200_OK