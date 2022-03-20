import re
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

images = UploadSet('images', IMAGES)

class NewsForm(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    is_private = BooleanField("Только для друзей") 
    submit = SubmitField('Применить')