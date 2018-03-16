""" App Manager """

from flask import Flask
from model import *
import re

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
#       play game -- game is a class, questions are a class (already)
#           GAME STEPS
#           play again?
#   exit (q at any time)

# Regular Expression comparisons for user input
UID_RE = re.compile(r'\w{1,8}')
PTS_RE = re.compile(r'[1-5]')

# Standard prompt hint for user input
PROMPT = "\n(enter your {} or 'q' to quit) "  # 'User ID', 'points', etc

# Program runs only while quitting is False
quitting = False


def analyze_input(input_s, input_t):
    """ Checks if user wants to quit; then if input matches its requirements.
        Returns None or True/False.

    """

    if input_s.lower() == 'q':
        quitting = True
        return None

    if input_t == 'uid':
        return UID_RE.fullmatch(input_s) is not None

    if input_t == 'pts':
        return PTS_RE.fullmatch(input_s) is not None

    return None


def greet_user():
    """ Greets user. """

    G_MSG = "Hello! I'm Alexa Trebec, host of Command Line Interview Jeopardy."
    G_MSG += "\nI'm so glad you're here. =D"
    print(G_MSG)
    return None


def dismiss_user():
    """ Says goodbye to user. """

    Q_MSG = "Thank you! Goodbye! =D"
    print(Q_MSG)
    return None


def request_store_username():
    """ Gets username from STDIN; stores it as global const; adds it to DB. """

    i = 0
    while i <= 3:
        if i == 0:
            usermsg = "What may I call you? "
            UID = raw_input(usermsg + PROMPT).format('User ID')
        elif 0 < i < 3:
            usermsg = "Please enter up to 8 ASCII alphanumeric characters."
            UID = raw_input(usermsg + PROMPT).format('User ID')
        else:
            print("I'm sorry you're having trouble. Try again soon.")
            UID = 'q'

        _move_on = analyze_input(UID, 'uid')
        if _move_on is None:
            return None
        elif _move_on is True:
            break
        else:
            i += 1

    User.create(UID)
    return None


