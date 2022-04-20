from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'webp', 'avif']
class UploadForm(FlaskForm):
    image = FileField('image', validators=[
         FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')
    ])
    recaptcha = RecaptchaField()