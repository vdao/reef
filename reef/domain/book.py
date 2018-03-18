class Book(object):
    def __init__(self, author, title):
        self.author = author
        self.title = title

    def __repr__(self):
        return "Book('{}', '{}')".format(self.author, self.title)

    def __eq__(self, o):
        return self.author == o.author and self.title == o.title

    def __hash__(self):
        return hash(self.author) + hash(self.title)
