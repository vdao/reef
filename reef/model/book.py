class Book():

    def __init__(self, author, title):
        self.author = author
        self.title = title

    def __repr__(self):
        return "Book(author='{}', title='{}')".format(self.author, self.title)
