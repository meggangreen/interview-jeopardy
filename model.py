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
        """ Inserts new record into the DB. Returns success/failure message and
            new object or None.

        """
        class_name = cls.__name__
        if not val:
            msg = "Cannot create {} with empty value. You submitted '{}'."
            record = None
        elif len(cls.get_record_objects(col, val)) == 0:
            new_item = cls(**kwargs)
            db.session.add(new_item)
            db.session.commit()
            msg = "New {} '{}' created!"
            record = new_item
        else:
            msg = ("Welcome back!" if class_name == 'User'
                   else "{} '{}' already exists.")
            record = None

        return (msg.format(class_name, val), record)


class Subject(Base):
    """ Subjects model; filled in the function 'seed_subjects'. """

    __tablename__ = 'subjects'

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Subject "{}">'.format(self.title)


    @classmethod
    def create(cls, title):
        """ Inserts new record into the DB. Prints success/failure message.
            Returns new object or None.

        """

        msg, record = super().create(col='title', val=title, title=title)
        print(msg)
        return record


    def edit(self, new_val=None):
        """ Change selected title in DB. """

        if len(Subject.get_record_objects(col='title', val=new_val)) > 0:
            print("Subject '{}' already exists.").format(new_val)
            return None
        else:
            self.title = new_val
            db.session.add(self)
            db.session.commit()
            print("Subject text changed!")
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
        self.qs_id = make_qs_id(q_id, s_id)
        self.q_id = q_id
        self.s_id = s_id

    def __repr__(self):
        return '<Q_Subj q_id={} s_id={}>'.format(self.q_id, self.s_id)


    @classmethod
    def create(cls, q_id, s_id):
        """ Inserts new record into the DB. Prints success/failure message.
            Returns None.

        """

        qs_id = make_qs_id(q_id, s_id)
        msg, record = super().create(col='qs_id', val=qs_id,
                                     q_id=q_id, s_id=s_id)
        print(msg)
        return None  # should never need to return this record


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
        self.difficulty = kwargs.get('difficulty', 2)
        self.durations = kwargs.get('durations', "180,")
        self.category = kwargs.get('category', "T")

    def __repr__(self):
        return '<Question id={} "{}">'.format(self.q_id, self.title[:60])


    @classmethod
    def create(cls, title, text, **kwargs):
        """ Inserts new record into the DB. Prints success/failure message.
            Returns new object or None.

        """

        msg, record = super().create(col='title', val=title,
                                     title=title, text=text, **kwargs)
        print(msg)
        return record


    def edit(self, new_val=None):
        """ Change selected title in DB. """

        if len(Question.get_record_objects(col='title', val=new_val)) > 0:
            print("Question '{}' already exists.").format(new_val[:50])
            return None
        else:
            self.title = new_val
            db.session.add(self)
            db.session.commit()
            print("Question title changed!")
            return None


    def add_subjects(self, new_subjs=[]):
        """ Initiates Q_Subj link for each subject in the list. """

        for new_subj in new_subjs:

            # Get Subject from DB
            subj = Subject.get_record_objects(col='title', val=new_subj)
            if not subj:
                y_or_n = raw_input("Subject '{}' does not exist. "
                                   .format(new_subj) +
                                   "Do you want to add it? (y/n) ")
                if y_or_n.lower() == 'y':
                    subj = Subject.create(new_subj)
                else:
                    print("Cannot add current subject; trying the next.")
                    continue
            else:
                subj = subj[0]

            Q_Subj.create(self.q_id, subj.s_id)

        return None


class User(Base):
    """ Users model. Users have IDs and scores. We don't need much on them. """

    __tablename__ = 'users'

    u_id = db.Column(db.Text, primary_key=True)
    scores = db.relationship('Score')

    def __init__(self, u_id):
        self.u_id = u_id

    def __repr__(self):
        return '<User "{}">'.format(self.u_id)


    @classmethod
    def create(cls, u_id):
        """ Inserts new record into the DB. Prints success/failure message.
            Returns new object or None.

        """

        msg, record = super().create(col='u_id', val=u_id, u_id=u_id)
        print(msg)
        return record


    def edit(self, new_val=None):
        """ Change selected u_id in DB. """

        if len(User.get_record_objects(col='u_id', val=new_val)) > 0:
            print("User '{}' already exists.").format(new_val)
            return None
        else:
            self.u_id = new_val
            db.session.add(self)
            db.session.commit()
            print("User ID changed!")
            return None


class Score(Base):
    """ Score model. Holds the various point levels (0 to 5) a user has scored
        on a specific question. The scores are stored text of a comma-separated
        list and kept in chronologogical order of least-to-most recent.
        Eg: u_id 4291 + q_id 375 >> '2,2,3,4,4,3,5,'
        Eg: u_id 4291 + q_id 573 >> '4,3,4,5,5,4,'
        Eg: u_id 1942 + q_id 375 >> '3,4,5,4,5,'

    """

    __tablename__ = 'scores'

    score_id = db.Column(db.Text, primary_key=True)
    u_id = db.Column(db.Text, db.ForeignKey('users.u_id'), nullable=False)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.q_id'), nullable=False)
    points = db.Column(db.Text, nullable=False, default='')  # '0,1,2,3,4,5,'

    def __init__(self, u_id, q_id):
        self.score_id = make_score_id(u_id, q_id)
        self.u_id = u_id
        self.q_id = q_id
        self.points = ''

    def __repr__(self):
        return '<Score u_id={} q_id={}>'.format(self.u_id, self.q_id)


    @classmethod
    def create(cls, u_id, q_id):
        """ Inserts new record into the DB. Doesn't print(success/failure)
            message. Returns new object or None.

        """

        score_id = make_score_id(u_id, q_id)
        msg, record = super().create(col='score_id', val=score_id,
                                     u_id=u_id, q_id=q_id)
        # don't print(msg)
        return record


    @classmethod
    def add_points(cls, u_id=None, q_id=None, new_points=None):
        """ Add new points value for user-question pair. Inserts new u-q pair
            into DB if necessary.

        """

        if not u_id or not q_id or new_points not in range(6):
            return None

        score_id = make_score_id(u_id, q_id)
        score = cls.get_record_objects(col='score_id', val=score_id)

        if not score:
            msg, score = cls.create(u_id=u_id, q_id=q_id)
        else:
            score = score[0]

        score.points += (str(new_points) + ",")
        db.session.add(score)
        db.session.commit()
        print("Scores updated!")

        return None


################################################################################
 ### Helper Functions ###

def make_qs_id(q_id, s_id):
    """ Makes Q_Subj id for all functions. """
    return int(str(q_id) + str(s_id))


def make_score_id(u_id, q_id):
    """ Makes score id for all functions. """
    return u_id + '--' + str(q_id)


################################################################################
 ### Database Functions ###

def connect_to_db(app):
    """ Connect the database to a Flask app. """

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cliijeopardy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def seed_data():
    """ Seed data """

    db.create_all()  # does nothing to already created tables
    seed_subjects()
    # questions with qs_subjs
    # users: add 'default'?

    return None


def seed_subjects():
    """ Reads subjects in from path. Original list brainstormed with amsowie. """

    with open('data/subjects.txt') as f:
        subjects = f.readlines()

    for subj in subjects:
        Subject.create(subj.strip())

    print("\n-- Finished seeding subjects. --\n")

    return None


if __name__ == '__main__':

    # Start Flask app
    from flask import Flask
    app = Flask(__name__)

    # Connect to DB
    connect_to_db(app)
    print("\n-- Working directly in database. Use Flask-SQLAlchemy syntax. --\n")
