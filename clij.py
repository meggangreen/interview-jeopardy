""" App Manager """

from flask import Flask
from model import *

# Start Flask app and connect to DB
app = Flask(__name__)
connect_to_db(app)

# Functions:
# start
#   enter username
#   check if db exists
#       no:
#           create
#            OR
#           quit
#   welcome user
#       user.create if necessary
#   rules
#       q at any time
#   while play == yes
#       play game
#           GAME STEPS
#           play again?
#   exit (q at any time)
