from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from reef.auth import login_required
from reef.model import *
from reef import database
from reef.forms.settings.import_form import ImportFileForm

import os
import io
import csv


bp = Blueprint('settings', __name__, url_prefix='/settings')

ALLOWED_EXTENSIONS = {'csv'}


def allowed_filename(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@bp.route('/')
@login_required
def index():
    return render_template('settings/index.html', books=(g.user.books))


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = ImportFileForm()
    if form.validate_on_submit():
        file = request.files['file']
        if file and allowed_filename(file.filename):
            models = []
            reader = csv.DictReader(io.TextIOWrapper(io.BytesIO(file.read())))
            for row in reader:
                model = Book(author=row.get('author', None),
                             title=row.get('title', None),
                             owner_id=g.user.id)
                database.session.add(model)

            database.session.commit()

        return redirect(url_for('books.index'))

    return render_template('settings/upload.html', form=form)
