""" ORM Models """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    """ Questions model """

    __tablename__ = 'questions'

    q_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Enum('1', '2', '3'), default='2',
                           index=True,
                           nullable=False)
    category_id = db.Column(db.String(1),
                            db.ForeignKey('categories.c_id'),
                            index=True,
                            nullable=False)
    subject_id = db.Column(db.Integer,
                           db.ForeignKey('subjects.s_id'),
                           index=True,
                           nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('questions', order_by='q_id'))
    subjects = db.relationship('Subject',
                               backref=db.backref('questions', order_by='q_id'))

    def __repr__(self):
        return ("""<Question id={} category={} subject={} difficulty={}
                             '{}'""").format(self.q_id,
                                             self.category.title,
                                             self.subject.title,
                                             self.difficulty,
                                             self.text[:50])

    @classmethod
    def do_something(cls):
        pass

    # category  # Behavioral, Coding, Theoretical
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
