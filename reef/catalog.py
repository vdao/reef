from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from reef.auth import login_required
from reef.model import *
from reef import database

bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@bp.route('/')
@login_required
def index():
    return render_template('catalog/index.html', books=(g.user.books))
