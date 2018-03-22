################################################################################
### Testing Module ###
# Tests Model and CLIJ modules -- assumes Flask-SQLAlchemy and SQLAlchemy teams
# have ensured their products work.
#
################################################################################

import unittest as UT
from model import *
from clij import *

# create database and seed functions for clijtest
def setUpModule():
    """ Seed test database. """

    # Start Flask app
    app = Flask(__name__)
    app.config['TESTING'] = True  # Shows verbose Flask error messages

    # Connect to DB
    connect_to_db(app)


def tearDownModule():
    """ Clear test database. """
    pass


class ModelHelperFuncsTests(UT.TestCase):

    def test_make_qs_id(self):
        """ Tests format and content of concatenated integer. """

        self.assertEqual(make_qs_id(1, 1), 11)
        self.assertEqual(make_qs_id(31, 217), 31217)


    def test_make_score_id(self):
        """ Tests format and content of concatenated string. """

        self.assertEqual(make_score_id('username', 7), 'username--7')


class ModelBaseMethods(UT.TestCase):

    def test_get_records(self):
        """ Returns a list based on a modified method of standard querying. """

        u_id = "default"
        u_obj = User.query.get(u_id)
        self.assertEqual(User.get_records(col='u_id', val=u_id), [u_obj])

        title = "test 193736"
        q_obj = Question.query.filter(Question.title == title).all()
        self.assertEqual(Question.get_records(col='title', val=title), q_obj)


class ModelQuestionMethods(UT.TestCase):

    def test_create(self):
        """ Tests creation and persistence of records, again relying on Flask-
            SQLAlchemy to be functional.

        """

        pass





if __name__ == '__main__':

    UT.main()
