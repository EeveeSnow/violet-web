"""
This script runs the Web_IDE application using a development server.
"""

from os import environ
import os
from random import randint
from violet_main import app
from waitress import serve


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    # PORT = randint(1000, 9999)
    PORT = 5000
    FLASK_ENV = "development"
    # app.run(HOST, PORT, debug=True)
    port = int(os.environ.get("PORT", 5000))
    serve(app, host='0.0.0.0', port=port)
        

   