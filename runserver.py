"""
This script runs the Web_IDE application using a development server.
"""

from os import environ
from random import randint
from violet_main import app


# if __name__ == '__main__':
HOST = environ.get('SERVER_HOST', 'localhost')
# PORT = randint(1000, 9999)
PORT = 5000
FLASK_ENV = "development"
app.run(HOST, PORT, debug=True)
        

   