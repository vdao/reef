from reef import database as db


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    notes = db.Column(db.String(1000))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    book_records = db.relationship('BookRecord', backref='reader', lazy='dynamic')