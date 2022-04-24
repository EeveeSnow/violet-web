from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp', 'avif']

class UploadForm(FlaskForm):
    image = FileField('image', validators=[
         FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')
    ])
    recaptcha = RecaptchaField()

class UploadForm2(FlaskForm):
    image = FileField('image', validators=[DataRequired(),
         FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')
    ])
#     recaptcha = RecaptchaField()
    submit = SubmitField('Применить')
