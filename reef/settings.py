from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from reef.auth import login_required
from reef.model import *
from reef import database
from reef.forms.settings.import_form import ImportFileForm
from reef.forms.settings.labels_form import PrintLabelsForm

import os
import io
import datetime
import csv
from barcode import generate
from barcode.pybarcode import ImageWriter
import base64
from fpdf import FPDF

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


@bp.route('/print_labels', methods=['GET', 'POST'])
@login_required
def print_labels():
    form = PrintLabelsForm()
    if form.validate_on_submit():
        page_width = 5
        page_height = 13
        last_code = form.start_from.data

        pdf = FPDF('P', 'mm', 'A4')
        pdf.set_margins(0, 0)

        files = []
        for p in range(0, form.page_count.data):
            pdf.add_page()
            for j in range(0, page_height):
                for i in range(0, page_width):
                    code = "%012d" % (last_code + 1,)
                    last_code += 1

                    f = barcode(code)
                    files.append(f)

                    pdf.image(f, x=scale(10 + i * 37), y=scale(11 + j * 20.6), w=scale(37), h=scale(16))

        tmpfile = os.path.join(current_app.config['GENERATED_FOLDER'],
                               'labels_{}.pdf'.format(datetime.datetime.now().timestamp()))
        pdf.output(tmpfile)

        for f in files:
            os.remove(f)

        return send_file(tmpfile)

    return render_template('settings/labels.html', form=form)


def calc_control(num):
    """
    Рассчитывает контрольное число кода EAN-13.

    Цифры набора нумеруются справа налево.
    Подсчитываются суммы цифр, стоящих на четных и нечетных местах.
    Сумма цифр, стоящих на четных местах, суммируется с утроенной суммой цифр, стоящих на нечетных местах.
    Если цифра единиц полученного результата равна нулю, то контрольная цифра — 0.
    Если последняя цифра результата не нуль, то контрольная цифра равна дополнению этой цифры до 10.

    :param num: число либо строка с первыми 12 числами
    :return: последнее контрольное число
    """
    rev = list(str(num))
    rev.reverse()
    sum_odd = sum([int(i) for i in rev[0::2]])
    sum_even = sum([int(i) for i in rev[1::2]])
    return (10 - ((sum_even + 3 * sum_odd) % 10)) % 10


def barcode(ean13):
    return generate('EAN13', str(ean13) + str(calc_control(ean13)), output='barcode_' + str(ean13), writer=ImageWriter(),
                    writer_options={'dpi': 160, 'text_distance': 1})


def scale(x):
    return x * 26.2 / 25.4


def to_pdf():
    pdf = FPDF('P', 'mm', 'A4')
    pdf.set_margins(0, 0)
    pdf.add_page()
    for i in range(0, 13):
        for j in range(0, 5):
            pdf.image('barcode_png.png', x=scale(10 + j * 37), y=scale(11 + i * 20.6), w=scale(37), h=scale(16))
    pdf.output('test.pdf')
