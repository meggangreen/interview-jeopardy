""" App Manager """

from flask import Flask
from model import *

# Start Flask app and connect to DB
app = Flask(__name__)
connect_to_db(app)


