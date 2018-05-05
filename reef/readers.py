from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from reef.auth import login_required
from reef.model import *
from reef import database

bp = Blueprint('readers', __name__, url_prefix='/readers')


@bp.route('/list')
@login_required
def index():
    return render_template('readers/index.html', readers=g.user.readers)
