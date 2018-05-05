from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class ImportFileForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Import')
