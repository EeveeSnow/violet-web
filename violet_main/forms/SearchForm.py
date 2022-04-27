from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = TextAreaField("Искать по имени", validators=[DataRequired()])
    submit = SubmitField('Искать')