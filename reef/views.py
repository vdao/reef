from flask import render_template, request
from model import Book


def home():
    return "Hello, world!"


def hello(name=None):
    return render_template('hello.html', name=name)


def book_add_form():
    return render_template('book_add.html')


def book_add():
    author = request.form.get('author', '')
    title = request.form.get('title', '')

    book = Book(author=author, title=title)
    book.put()

    return render_template('book_add.html', status="success! entity={}"
                           .format(book.__repr__()))
