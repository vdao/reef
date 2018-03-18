from google.appengine.ext import ndb


class Book(ndb.Model):
    author = ndb.StringProperty()
    title = ndb.StringProperty()

    def __repr__(self):
        return "Book(author='{}', title='{}')".format(self.author, self.title)
