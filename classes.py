""" Non-DB Python Classes """

from random import choice

class Game(obj):
    """ Game class. """

    # attrs:
    #   behavioral_q_set {}
    #   theoretical_q_set {}
    #   coding_q_set {}
    #   g_id 0-9
    #
    # methods:
    #   get_questions
    #   play

    def __init__(self, g_id):
        self.g_id = g_id
        self.behavioral_q_set = QuestionSet(category='B')
        self.theoretical_q_set = QuestionSet(category='T')
        self.coding_q_set = QuestionSet(category='C')


    def __repr__(self):
        return '<Game g_id={}>'.format(self.g_id)


class QuestionSet(obj):
    """ Question set. """

    def __init__(self, category):
        self.category = category
        get_question_rules()
        get_questions()


    def __repr__(self):
        return '<QuestionSet category={}>'.format(self.category)


    def get_questions(self):
        """ Get set of questions for a particular category. Each category has
            difficulty and quantity rules.

        """

        q_set = set([])
        total, easy, med, hard = self.q_rules
        remain = total

        q_pool = Question.query
                         .filter(Question.category == self.category)
                         .all()

        while easy > 0:

            easy += -1


        self.questions = q_set


    def get_question_rules(self):
        """ Return tuple of question quantity rules. """

        # Q Rules: ( total, difficulty: quantity )
        # eg: (6, 1, 1, 0) => 6 level value total, 1+ easy, 1+ medium, 0+ hard
        if self.category == 'B':
            q_rules = (6, 1, 1, 0)
        elif self.category == 'T':
            q_rules = (9, 1, 1, 0)
        elif self.category == 'C':
            q_rules = (9, 2, 2, 0)

        self.q_rules = q_rules
