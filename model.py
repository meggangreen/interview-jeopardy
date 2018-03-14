""" ORM Models """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################################################################################
### Classes ###

class Base(db.Model):
    """ Holds repeated class methods for the DB tables. """

    __abstract__ = True

    @classmethod
    def get_record_objects(cls, col=None, val=None):
        """ Given 'col' as column name and 'val' as entire and exact value to
            search, checks if any matching record is in DB. Returns list of objs.

        """

        if not col or not val:
            return []

        return cls.query.filter(cls.__table__.columns.get(col) == val).all()


    @classmethod
    def create(cls, col, val, **kwargs):
        """ Inserts new record into the DB. Returns new object or None. """

        if len(cls.get_record_objects(col, val)) == 0:
            new_item = cls(**kwargs)
            db.session.add(new_item)
            db.session.commit()
            return new_item
        else:
            return None


class Subject(Base):
    """ Subjects model; filled in the function 'seed_subjects'. """

    __tablename__ = 'subjects'

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return ('<Subject "{}">').format(self.title)


    @classmethod
    def create(cls, title):
        """ Inserts new record into the DB. Returns new object or None. """

        record = super(Subject, cls).create(col='title',
                                            val=title,
                                            title=title)
        if not record:
            print "Subject '{}' already exists.".format(title)
            return None
        else:
            print "New subject '{}' created!".format(title)
            return record


    def edit(self, new_val=None):
        """ Change selected title in DB. """

        if len(Subject.get_record_objects(col='title', val=new_val)) > 0:
            print "Subject '{}' already exists.".format(new_val)
            return None
        else:
            self.title = new_val
            db.session.add(self)
            db.session.commit()
            print "Subject text changed!"
            return None


class Q_Subj(Base):
    """ Association table to manage many-to-many relationship between Subjects
        and Questions.

    """

    __tablename__ = 'qs_subjs'

    qs_id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('subjects.s_id'), nullable=False)

    def __init__(self, s_id, q_id):
        self.qs_id = int(str(s_id) + str(q_id))
        self.q_id = q_id
        self.s_id = s_id

    def __repr__(self):
        return ('<Q_Subj q_id={} s_id={}>').format(self.q_id, self.s_id)


    @classmethod
    def create(cls, q_id, s_id):
        """ Inserts new record into the DB. Returns new object or None. """

        qs_id = int(str(s_id) + str(q_id))
        record = super(Q_Subj, cls).create(col='qs_id',
                                           val=qs_id,
                                           qs_id=qs_id)
        if not record:
            print "Question {} + Subject {} already linked.".format(q_id, s_id)
            return None
        else:
            print "Question {} + Subject linked!".format(q_id, s_id)
            return None


class Question(Base):
    """ Questions model """

    __tablename__ = 'questions'

    q_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False, default=2)  # 1, 2, 3
    durations = db.Column(db.Text, nullable=False, default="180,")  # '120,60,'
    category = db.Column(db.String(1), nullable=False, default="T")  # B, T, C
    subjects = db.relationship('Subject',
                               order_by='Subject.s_id',
                               secondary='qs_subjs',
                               backref=db.backref('questions', order_by=q_id))

    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text
        self.difficulty = difficulty if difficulty else 2
        self.durations = durations if durations else "180,"
        self.category = category if category else "T"

    def __repr__(self):
        return ('<Question id={} "{}">').format(self.q_id, self.title[:60])

    @classmethod
    def create(cls, title, text, **kwargs):
        """  """

        record = super(Question, cls).create(col='title',
                                             val=title,
                                             text=text,
                                             difficulty=difficulty,
                                             durations=durations,
                                             category=category)
        if not record:
            print "Question '{}' already exists.".format(title[:50])
            return None
        else:
            print "Question '{}' created!".format(title[:50])
            return record


    def edit(self, new_val=None):
        """ Change selected title in DB. """

        if len(Question.get_record_objects(col='title', val=new_val)) > 0:
            print "Question '{}' already exists.".format(new_val[:50])
            return None
        else:
            self.title = new_val
            db.session.add(self)
            db.session.commit()
            print "Question title changed!"
            return None


    def add_subjects(self, new_subjs=[]):
        """ Initiates Q_Subj link for each subject in the list. """

        for new_subj in new_subjs:

            # Get Subject from DB
            subj = Subject.get_record_objects(col='title', val=new_subj)[0]
            if not subj:
                y_or_n = rawinput("Subject '{}' does not exist. " +
                                  "Do you want to add it? (y/n) "
                                  .format(new_subj))
                if y_or_n.lower() == 'y':
                    subj = Subject.create(title)
                else:
                    print "Current subject cannot be added; trying the next."
                    continue

            Q_Subj.create(self.q_id, subj.s_id)

        return None


class User(Base):
    """ Users model. Users have IDs and scores. We don't need much on them. """

    __tablename__ = 'users'

    u_id = db.Column(db.Text, primary_key=True)
    scores = db.relationship('Scores')

    def __init__(self, u_id):
        self.u_id = u_id

    def __repr__(self):
        return ('<User "{}">').format(self.u_id)


    @classmethod
    def create(cls, u_id):
        """ Inserts new record into the DB. Returns new object or None. """

        record = super(User, cls).create(col='u_id',
                                         val=u_id,
                                         u_id=u_id)
        if not record:
            print "User '{}' already exists.".format(u_id)
            return None
        else:
            print "New user '{}' created!".format(u_id)
            return record


    def edit(self, new_val=None):
        """ Change selected u_id in DB. """

        if len(User.get_record_objects(col='u_id', val=new_val)) > 0:
            print "User '{}' already exists.".format(new_val)
            return None
        else:
            self.u_id = new_val
            db.session.add(self)
            db.session.commit()
            print "User ID changed!"
            return None


class Scores(Base):
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
        """ Add new points value for user-question pair. Inserts new u-q pair
            into DB if necessary.

        """

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
