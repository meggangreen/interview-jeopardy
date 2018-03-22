""" App Manager """

from flask import Flask
import re
from model import *

# Functions:
# [ ]start
#   [-]greet
#   [-]enter username
#   [ ]check if db exists
#       [ ]no:
#           [ ]create
#            OR
#           [ ]quit
#   [-]welcome user
#       [-]user.create if necessary
#   [ ]rules
#       [ ]q at any time
#   [ ]while play == yes
#       [ ]play game -- game is a class, questions are a class (already)
#           [ ]GAME STEPS
#           [ ]play again? change user?
#   [-]exit (q at any time)

def run_session():
    """ Game manager. """

    # Clear Console

    greet_user()

    game_session['USER'] = get_username()
    if not game_session['QUIT']:
        User.create(game_session['USER'])

    while not game_session['QUIT']:
        game_session['GNUM'] += 1
        print("\n\n-- Instantiate Game " + str(game_session['GNUM']) + " --")
        # game = Game(id=game_session['GNUM'])  # instantiation gets question set
        print("-- Start Game with 'game.play' --")
        # game.play()
        if game_session['QUIT']:
            break
        is_continue()

    dismiss_user()

    return None


def analyze_input(input_string, input_type):
    """ Checks if user wants to quit; then if input matches its requirements.
        Returns None or True/False.

    """

    if input_string.lower() == 'q':
        game_session['QUIT'] = True
        return None

    if input_type == 'uid':
        return UID_RE.fullmatch(input_string) is not None

    if input_type == 'pts':
        return PTS_RE.fullmatch(input_string) is not None

    if input_type == 'other':
        return None

    return None


def greet_user():
    """ Greets user. """

    G_MSG = "Hello! I'm Alexa Trebec, host of Command Line Interview Jeopardy."
    G_MSG += "\nI'm so glad you're here. =D"
    print('\n\n' + G_MSG)
    return None


def dismiss_user():
    """ Says goodbye to user. """

    Q_MSG = "Thank you! Goodbye! =D"
    print('\n' + Q_MSG + '\n\n')
    return None


def get_username():
    """ Gets username from STDIN; returns it for storage. """

    i = 0
    while i <= 3:
        if i == 0:
            usermsg = "\nWhat may I call you? "
            UID = input(usermsg + PROMPT.format('your User ID'))
        elif 0 < i < 3:
            usermsg = "\nOops! Please enter up to 8 ASCII alphanumeric characters."
            UID = input(usermsg + PROMPT.format('your User ID'))
        else:
            print("\nI'm sorry you're having trouble. Try again soon.")
            UID = 'q'

        success = analyze_input(UID, 'uid')
        if success is None:
            return None
        elif success is True:
            break
        else:
            i += 1

    return UID


def is_continue():
    """ Ask user if they want to continue. Force quits if game count is 10. """

    # Future versions could analyze game's questions' scores for 'good job!' msg

    if game_session['GNUM'] == 2:
        game_session['QUIT'] = True
        print("\nWow {}! That was so good! ".format(game_session['USER']) +
              "I've got to run, but let's play again soon, okay?")
    else:
        usermsg = ("\nThat was fun! =D Could we play again, {}? "
                   .format(game_session['USER']))
        other = input(usermsg + PROMPT.format("'y' to continue"))
        analyze_input(other, 'other')

    return None


################################################################################
### Run App ###

if __name__ == '__main__':

    # Start Flask app and connect to DB
    app = Flask(__name__)
    # app.secret_key = "Command Line Interview Jeopardy"
    connect_to_db(app)

    # Regular Expression comparisons for user input
    UID_RE = re.compile(r'^\w{1,8}$')
    PTS_RE = re.compile(r'^[1-5]$')

    # Standard prompt hint for user input
    PROMPT = "\n(enter {} or 'q' to quit) "  # 'your User ID', 'the points', etc

    # Program runs only while quitting is False
    # global _quit
    game_session = {'QUIT': False,
                    'USER': None,
                    'GNUM': 0}

    # Start game session
    run_session()
