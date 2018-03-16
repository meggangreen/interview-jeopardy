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

PROMPT = "(enter your {} or 'q' to quit) "  # 'User ID', 'points', etc
quitting = False
q_msg = "Thank you! Goodbye! =D"

def analyze_input(input_s, input_t):
    """ Checks if user wants to quit; then if input matches its requirements. """

    if input_s.lower() == 'q':
        quitting = True
        return None

    if re.

    sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6

    return


def request_and_store_username():
    """ Gets username from STDIN. Stores as global const. """

    GREET = "Hello! I'm Alexa Trebec, the host of Command Line Interview Jeopardy."
    GREET += "\nI'm so glad you're here. =D"
    print GREET

    i = 0
    while i <= 3:
        if i == 0:
            usermsg = "What may I call you? "
            UID = raw_input(usermsg + PROMPT).format('User ID')
        elif UID == 'q':
            quitting = True
            return None
        elif is_safe_text(UID) is True:
            # store global
            # break
        elif i == 3:
            q_msg = "I'm sorry you're having trouble. Try again soon. Goodbye!"
            quitting = True
            return None
        else:


