from reef import database as db
from datetime import datetime


class BookRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
