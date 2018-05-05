from reef import database as db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    books = db.relationship('Book', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
