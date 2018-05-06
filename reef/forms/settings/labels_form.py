from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class PrintLabelsForm(FlaskForm):
    start_from = IntegerField('Start from', validators=[DataRequired()])
    page_count = IntegerField('Page count', validators=[DataRequired()])
    submit = SubmitField('Download')
