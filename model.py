""" ORM Models """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

### Classes ###

class Category(db.Model):
    """ Categories model

        The rows for Behavioral, Coding, Theoretical are filled in the function
        seed_categories.

    """

    __tablename__ = 'categories'

    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)


class Subject(db.Model):
    """ Subjects model

        The rows are filled in the function 'seed_subjects'.

    """

    __tablename__ = 'subjects'

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)


class Question(db.Model):
    """ Questions model """

    __tablename__ = 'questions'

    q_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)  # 1, 2, 3
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.c_id'),
                            index=True,
                            nullable=False)
    # subject_id = db.Column(db.Integer,
    #                        db.ForeignKey('subjects.s_id'),
    #                        index=True,
    #                        nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('questions'))
    # subjects = db.relationship('Subject',
    #                            backref=db.backref('questions'))

    def __repr__(self):
        return ("<Question id={} category={} subject={} difficulty={}\n" +
                " " * 10 + "text: '{}'>").format(self.q_id,
                                                 self.category.title,
                                                 self.subjects,
                                                 self.difficulty,
                                                 self.text[:50])

    @classmethod
    def do_something(cls):
        pass

    # category  #
    # subject


def connect_to_db(app):
    """ Connect the database to the Flask app. """

    # Configure to use PostgreSQL production database
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
