from flask import Flask

app = Flask(__name__)

from src import counter  # Ensure you import the routes
from src.counter import app  # Expose Flask app for testing
