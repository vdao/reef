from reef import database as db
from datetime import datetime


class BookRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('reader.id'), nullable=False)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('book_records', lazy='dynamic'))