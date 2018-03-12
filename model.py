""" ORM Models """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################################################################################
### Classes ###

class Subject(db.Model):
    """ Subjects model; filled in the function 'seed_subjects'. """

    __tablename__ = 'subjects'

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)


class Q_Subj(db.Model):
    """ Association table to manage many-to-many relationship between Subjects
        and Questions.

    """

    __tablename__ = 'qs_subjs'

    qs_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_id = db.Column(db.Integer, db.ForeignKey('subjects.s_id'), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'), nullable=False)


class Question(db.Model):
    """ Questions model """

    __tablename__ = 'questions'

    q_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False, default=2)  # 1, 2, 3
    durations = db.Column(db.Text, nullable=False, default="120,")
    category = db.Column(db.String(1), nullable=False)  # B, T, C
    subjects = db.relationship('Subject',
                               order_by='Subject.s_id',
                               secondary='qs_subjs',
                               backref=db.backref('questions', order_by=q_id))

    def __repr__(self):
        return ('<Question id={} "{}">').format(self.q_id, self.title[:60])

    @classmethod
    def do_something(cls):
        pass

    # category  #
    # subject


class User(db.Model):
    """ Users model. Users have IDs and scores. We don't need much on them. """

    __tablename__ = 'users'

    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scores = db.relationship('Scores')


class Scores(db.Model):
    """ Scores model. Holds the various point levels (0 to 5) a user has scored
        on a specific question. The scores are presented as a comma-separated
        list and kept in chronologogical order of least-to-most recent.
        Eg: u_id 4291 + q_id 375 >> '2,2,3,4,4,3,5'
        Eg: u_id 4291 + q_id 573 >> '4,3,4,5,5,4'
        Eg: u_id 1942 + q_id 375 >> '3,4,5,4,5'

    """

    __tablename__ = 'scores'

    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey('users.u_id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)  # 0 to 5
    count = db.Column(db.Integer, nullable=False, default=0)


################################################################################
### Functions ###

def connect_to_db(app):
    """ Connect the database to the Flask app. """

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cliijeopardy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)





if __name__ == '__main__':

    # Start Flask app
    from flask import Flask
    app = Flask(__name__)

    # Work directly with DB
    connect_to_db(app)
    print "\n\nConnected to DB.\n"

    # Create and seed database, if necessary
    db.create_all()
    # seed_data()
