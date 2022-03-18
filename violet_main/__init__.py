"""
The flask application package.
"""

import datetime
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IDE'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365)

import violet_main.views
