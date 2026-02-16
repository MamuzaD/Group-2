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
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['GET'])
def nonexistent_counter(name):
    if not counter_exists(name):
        return jsonify({"error": f"Counter {name} is nonexistent"}), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    # i have purposefully not included a check for if the counter already exists
    # this is because student 8 will need to implement this :)

    COUNTERS.pop(name)
    return jsonify({name: name}), status.HTTP_204_NO_CONTENT