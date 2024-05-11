import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    '''
        Set config variables for the flask app
        Using Environment variables where available.
        Otherwise create the config variable if not done already
    '''

    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ryan will never get access to my CSS'
    # Update the SQLALCHEMY_DATABASE_URI to use the new ElephantSQL URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://veyyndoc:koJIbpOUNhy7ks9TqfWH8tbXyYiN3u-K@stampy.db.elephantsql.com/veyyndoc'
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
