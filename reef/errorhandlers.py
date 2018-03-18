from reef import app
from flask import render_template


def page_not_found(error):
    return render_template('404.html')


app.register_error_handler(404, page_not_found)
