"""
The flask application package.
"""

import datetime
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'messendger'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365)
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LdGbYkfAAAAAF3RAa4OULbd1fa2EFXHCCa-FrL3"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LdGbYkfAAAAAPFLnGwT90iHtt_xF7N8LoaV-sHm"





import violet_main.views
