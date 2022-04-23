from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewsForm(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    is_private = BooleanField("Только для друзей") 
    submit = SubmitField('Применить')
