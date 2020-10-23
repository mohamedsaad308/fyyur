import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
ENV = "prod"
# Connect to the database
if ENV = "dev":
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2941@localhost:5432/fyyur'
else:
    SQLALCHEMY_DATABASE_URI = "postgres://fqorpfkkidncet:9f756a8547563910c01518f6abc407a3ac33212dabe895e4ed9338bc8f5bb393@ec2-52-72-34-184.compute-1.amazonaws.com:5432/da80o58c4kqkvv"

# TODO IMPLEMENT DATABASE URL

class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
