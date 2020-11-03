import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
ENV = "prod"
# Connect to the database
if ENV == "dev":
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_DEV')
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# TODO IMPLEMENT DATABASE URL

class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
