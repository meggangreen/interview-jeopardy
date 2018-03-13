""" ORM Models """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################################################################################
### Classes ###

class Base(db.Model):
    """ Holds repeated class methods for the DB tables. """

    @classmethod
    def is_in_db(cls, idn=None):
        """ Checks if record is in DB. """

        if not idn:
            return None

        return cls.query.get(idn) is not None


class Subject(db.Model):
    """ Subjects model; filled in the function 'seed_subjects'. """

    __tablename__ = 'subjects'

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return ('<Subject "{}">').format(self.title)


class Q_Subj(db.Model):
    """ Association table to manage many-to-many relationship between Subjects
        and Questions.

    """

    __tablename__ = 'qs_subjs'

    qs_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_id = db.Column(db.Integer, db.ForeignKey('subjects.s_id'), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'), nullable=False)

    def __init__(self, s_id, q_id):
        self.s_id = s_id
        self.q_id = q_id

    def __repr__(self):
        return ('<Q_Subj s_id={} q_id={}>').format(self.s_id, self.q_id)


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

    u_id = db.Column(db.Text, primary_key=True)
    scores = db.relationship('Scores')

    def __init__(self, u_id):
        self.u_id = u_id

    def __repr__(self):
        return ('<User "{}">').format(self.u_id)


    @classmethod
    def is_user(cls, u_id=None):
        """ Checks if user id is in DB. """

        if not u_id:
            return None

        return 0 < len(cls.query.filter(cls.u_id == u_id).all())


    @classmethod
    def create_user(cls, u_id):
        """ Add new user to the DB. """

        if cls.is_user(u_id) is True:
            print "The user '{}' already exists.".format(u_id)
            return None
        elif cls.is_user(u_id) is False:
            new_user = User(u_id)
            db.session.add(new_user)
            db.session.commit()
            print "New user '{}' created!".format(u_id)
            return new_user


    @classmethod
    def get_user(cls, u_id):
        """ Retrieve User object from DB. """

        if cls.is_user(u_id) is True:
            return cls.query.get(u_id)


    def change_user_id(self, new_id=None):
        """ Change selected u_id in DB. """

        if User.is_user(new_id) is True:
            print "The user '{}' already exists.".format(new_id)
            return None
        elif User.is_user(new_id) is False:
            self.u_id = new_id
            db.session.add(self)
            db.session.commit()
            print "User ID changed!"
            return None


class Scores(db.Model):
    """ Scores model. Holds the various point levels (0 to 5) a user has scored
        on a specific question. The scores are stored text of a comma-separated
        list and kept in chronologogical order of least-to-most recent.
        Eg: u_id 4291 + q_id 375 >> '2,2,3,4,4,3,5,'
        Eg: u_id 4291 + q_id 573 >> '4,3,4,5,5,4,'
        Eg: u_id 1942 + q_id 375 >> '3,4,5,4,5,'

    """

    __tablename__ = 'scores'

    score_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Text, db.ForeignKey('users.u_id'), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'), nullable=False)
    points = db.Column(db.Text, nullable=False, default='')  # '0,1,2,3,4,5,'

    def __init__(self, u_id, q_id):
        self.u_id = u_id
        self.q_id = q_id
        self.points = ''

    def __repr__(self):
        return ('<Score u_id={} q_id={}>').format(self.u_id, self.q_id)

    @classmethod
    def add_new_points(cls, u_id=None, q_id=None, new_points=None):
        """ Add new points value for user-question pair. """

        if not u_id or not q_id or not new_points or new_points not in range(6):
            return None

        score = cls.query.filter(cls.u_id == u_id, cls.q_id == q_id).first()
        if not score:
            score = Score(u_id=u_id, q_id=q_id)

        score.points += (str(new_points) + ",")
        db.session.add(score)
        db.session.commit()


################################################################################
### Functions ###

def connect_to_db(app):
    """ Connect the database to a Flask app. """

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cliijeopardy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def seed_data():
    """ Seed data """

    # subjects first (qs dependent) - brainstorm list with amsowie
    # questions with qs_subjs
    # users: add 'default'

    pass


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
