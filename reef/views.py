from flask import render_template


def home():
    return "Hello, world!"


def hello(name=None):
    return render_template('hello.html', name=name)
