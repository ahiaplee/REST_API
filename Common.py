""" Common imports and shared variables used by the program

- Not meant to be run as a script

"""
from flask import Flask
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from configparser import ConfigParser

import datetime
import jwt
import psycopg2
import base64
import os

from Message import Message
from User import User
from Database import DatabaseConnection
from celery import Celery

def CheckArgs(toCheck, args):
    """
    Check if a parameter is missing from the given given arguments

    Args:
        toCheck: master list of arguments to check (array)
        args : arguments parsed from requestion (dictionary)
    Returns:
        - Message Object if parameter is missing
        - True if no missing parameters found
    """
    for key in toCheck:
        if args[key] is None:
            msg = 'Parameter %s missing' % key
            return Message(False, msg)

    return True

#shared variables
app = Flask(__name__)
app.name = "MY_REST_API"
print(app.name)
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['result_backend'] = 'redis://redis:6379/0'
api = Api(app)
dbObject = DatabaseConnection()
UPLOAD_DIR = os.getcwd() + "/Files"


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if __name__ == '__main__':
    pass