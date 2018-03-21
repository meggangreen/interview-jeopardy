import unittest as UT
from model import *
from clij import *

class ModelHelperFuncsTests(UT.TestCase):

    def test_make_qs_id(self):
        """ Returns integer. """

        self.assertEqual(make_qs_id(1, 1), 11)


    def test_make_score_id(self):
        """ Returns concatenated string. """

        self.assertEqual(make_score_id('username', 7), 'username--7')


class ModelClassMethods(UT.TestCase):

    # create data and seed functions for clijtest

    def test_get_record_objects(self):
        """ Returns a list based on a modified method of standard querying.

            We leave it to Flask-SQLAlchemy and SQLAlchemy teams to ensure their
            products work. We test that our modified query gets the same record
            object as the regular query.

        """

        u_id = "default"
        u_obj = User.query.get(u_id)
        self.assertEqual(User.get_record_objects(col='u_id', val=u_id), [u_obj])





if __name__ == '__main__':

    # Start Flask app
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True  # Shows verbose DB error messages

    # Connect to DB
    connect_to_db(app)
    db.create_all()  # does nothing to already created tables

    UT.main()
