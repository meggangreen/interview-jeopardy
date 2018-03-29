""" Non-DB Python Classes """

from random import choice, sample
from model import *

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
        self._behavioral_q_set = QuestionSet(category='B')
        self._theoretical_q_set = QuestionSet(category='T')
        self._coding_q_set = QuestionSet(category='C')


    def __repr__(self):
        return '<Game g_id={}>'.format(self._g_id)


class QuestionSet(object):
    """ Question set. """

    def __init__(self, category):
        self._category = category
        self._q_rules = self._get_question_rules()
        self._questions = None  # self._get_questions()


    def __repr__(self):
        return '<QuestionSet category={}>'.format(self._category)


    def _get_questions(self):
        """ Get set of questions for a particular category. Each category has
            difficulty and quantity rules.

        """

        q_set = set([])
        remain, easy_count, med_count, hard_count = self._q_rules
        category = self._category

        easy_pool = set(Question.query
                                .filter(Question.category == category,
                                        Question.difficulty == 1)
                                .all())
        med_pool = set(Question.query
                               .filter(Question.category == category,
                                       Question.difficulty == 2)
                               .all())
        hard_pool = set(Question.query
                                .filter(Question.category == category,
                                        Question.difficulty == 3)
                                .all())

        if easy_count > 0:
            q_objs = sample(easy_pool, easy_count)
            q_set.update(q_objs)
            easy_pool.difference_update(q_objs)
            remain -= 1 * easy_count

        if med_count > 0:
            q_objs = sample(med_pool, med_count)
            q_set.update(q_objs)
            med_pool.difference_update(q_objs)
            remain -= 1 * med_count

        if hard_count > 0:
            q_objs = sample(hard_pool, hard_count)
            q_set.update(q_objs)
            hard_pool.difference_update(q_objs)
            remain -= 1 * hard_count

        # Combine all remaining questions into one pool
        q_pool = easy_pool | med_pool | hard_pool

        while remain > 0 and len(q_pool) > 0:
            q_obj = sample(q_pool, 1)[0]
            q_set.add(q_obj)
            q_pool.remove(q_obj)
            remain -= q_obj.difficulty

        return q_set


    def _get_question_rules(self):
        """ Return tuple of question quantity rules. """

        # Q Rules: ( total, easy_count, med_count, hard_count )
        # eg: (6, 1, 1, 0) => 6 level value total, 1+ easy, 1+ medium, 0+ hard
        if self._category == 'B':
            q_rules = (6, 1, 1, 0)
        elif self._category == 'T':
            q_rules = (9, 1, 1, 0)
        elif self._category == 'C':
            q_rules = (9, 2, 2, 0)

        return q_rules
