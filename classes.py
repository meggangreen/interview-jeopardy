""" Non-DB Python Classes """

from random import sample
from model import *
from clij import analyze_input

class Game(object):
    """ Game class. """

    # methods:
    #   play

    def __init__(self, g_id):
        """ Initializes a game.

        @param g_id:      The game id, an integer 0 to 9, as set by run_session
        @param *_q_set:   A set of Questions with category B, T, or C

        """

        self._g_id = g_id

        # Get question sets from database
        self._question_sets = [QuestionSet(category='B'),
                               QuestionSet(category='T'),
                               QuestionSet(category='C')]


    def __repr__(self):
        return '<Game g_id={}>'.format(self._g_id)


    def _play(self):
        """  """

        print("\nLet's get started!")

        for q_set in self._question_sets:

            if not game_session['QUIT']:
                q_set._ask()

        return None


class QuestionSet(object):
    """ Question set. """

    def __init__(self, category):
        """ Initializes a question set.

            @param q_rules:    A tuple of the total number of difficulty points
                               and minimum quantities of easy, medium, and hard
                               questions.
                               IE: ( total, easy_min, med_min, hard_min )
                               EG: (6, 1, 1, 0) => 6 total difficulty points,
                                                   at least 1 easy question,
                                                   at least 1 medium question,
                                                   no minimum of hard questions.
            @param questions:  The set of questions to be asked.

        """

        if category == 'B':
            self._name = "Behavioral"
        elif category == 'T':
            self._name = "Theoretical"
        elif category == 'C':
            self._name == "Coding"
        self._category = category
        self._q_rules = self._get_question_rules()
        self._questions = self._get_all_questions()


    def __repr__(self):
        return '<QuestionSet {}>'.format(self._name)


    def _get_all_questions(self):
        """ Get set of questions for a particular category. Each category has
            difficulty and quantity rules.

        """

        q_set = set([])
        q_pool = set([])
        remain = self._q_rules[0]

        # Where i is a difficulty level 1 to 3
        for i in range(1,4):
            quantity = self._q_rules[i]
            d_using, d_pool = self._get_questions_by_difficulty(i, quantity)
            q_set.update(d_using)
            q_pool.update(d_pool)
            remain -= i * len(d_using)

        # Fill q_set from q_pool until no difficulty points remain
        while remain > 0 and q_pool:
            q_obj = sample(q_pool, 1)[0]
            q_set.add(q_obj)
            q_pool.remove(q_obj)
            remain -= q_obj.difficulty

        return q_set


    def _get_questions_by_difficulty(self, level, quantity):
        """  """

        q_pool = set(Question.query
                             .filter(Question.category == self._category,
                                     Question.difficulty == level)
                             .all())

        # Put minimum number of each type of question into q_using;
        # remove selected questions from q_pool
        # Skip if no question of category and difficulty exists;
        # modify the count if not enough questions exist
        if quantity > 0 and q_pool:
            if len(q_pool) < quantity:
                quantity = len(q_pool)
            q_using = sample(q_pool, quantity)
            q_pool.difference_update(q_using)
        else:
            q_using = []

        return (q_using, q_pool)


    def _get_question_rules(self):
        """ Return tuple of question quantity rules. """

        if self._category == 'B':
            q_rules = (6, 1, 1, 0)
        elif self._category == 'T':
            q_rules = (9, 1, 1, 0)
        elif self._category == 'C':
            q_rules = (9, 2, 2, 0)

        return q_rules


    def _ask(self):
        """  """

        ready = input("Are you ready for the {} questions?"
                      .format(self._name) +
                      PROMPT.format("'y' to continue, 's' to skip,"))
        analyze_input(ready, other)

        if not game_session['QUIT']:
            for question in self._questions:
                if question.difficulty == 1:
                    first = question
                    self._questions.remove(first)
                    break

        while not game_session['QUIT'] and self._questions:
            if first:
                curr_q = first
                del first
            else:
                curr_q = self._questions.pop()
            curr_q._ask()
            points = input("Evaluate your answer and enter your score." +
                           PROMPT.format("your points 1 to 5"))
            if
            Score.add_points()



