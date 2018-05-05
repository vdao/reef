from reef import database as db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('categories', lazy='dynamic'))

    def __repr__(self):
        return "Category(id='{}', name={})".format(self.id, self.name)
