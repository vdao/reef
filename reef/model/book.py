from reef import database as db
from datetime import datetime


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(300))
    title = db.Column(db.String(300))
    description = db.Column(db.String(1000))
    code = db.Column(db.String(30), index=True, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_record = db.relationship('BookRecord', backref='book', lazy='dynamic')

    def __repr__(self):
        return "Book(id='{}', author='{}', title='{}')".format(
            self.id, self.author, self.title)
