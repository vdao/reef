from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from reef.auth import login_required
from reef.model import *
from reef import database

import flask

bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    items_per_page = flask.current_app.config['ITEMS_PER_PAGE']
    page_content = g.user.books.paginate(page, items_per_page, False)
    next_url = url_for('books.index', page=page_content.next_num) \
        if page_content.has_next else None
    prev_url = url_for('books.index', page=page_content.prev_num) \
        if page_content.has_prev else None

    return render_template('books/index.html', books=page_content.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error, 'danger')
        else:
            post = Post(title=title, body=body, author=g.user)
            database.session.add(post)
            database.session.commit()
            return redirect(url_for('books.index'))

    return render_template('books/create.html')


def get_post(id, check_author=True):
    post = Post.query.get(id)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post.author.id != g.user.id:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error, 'danger')
        else:
            database.session.query(Post).filter(Post.id == id) \
                .update({'title': title, 'body': body})
            database.session.commit()
            return redirect(url_for('books.index'))

    return render_template('books/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    database.session.query(Post).filter(Post.id == id).delete()
    database.session.commit()
    return redirect(url_for('books.index'))
