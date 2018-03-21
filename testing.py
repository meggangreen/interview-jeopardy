import unittest as UT
from model import *
from clij import *

class ModelHelperFuncsTests(UT.TestCase):

    def test_make_qs_id(self):
        """ Returns integer. """

        assert make_qs_id(1, 1) == 11


    def test_make_score_id(self):
        """ Returns concatenated string. """

        assert make_score_id('username', 7) == 'username--7'


class ModelClassMethods(UT.TestCase):

    # create data and seed functions for clijtest

    def test_get_record_objects(self):
        """ Returns a list. """

        test_q = Question.query.get(1)
        assert Question.get_record_objects(col='q_id', val=1) == [test_q]





if __name__ == '__main__':

    # Start Flask app
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True  # Shows verbose debugging

    # Connect to DB
    connect_to_db(app)
    db.create_all()  # does nothing to already created tables

    UT.main()
