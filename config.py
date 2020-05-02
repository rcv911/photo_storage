import os
basedir = os.path.abspath(os.path.dirname(__file__))

DB_HOST = 'localhost'
DB_PORT = 5454
DB_USERNAME = 'postgres'
DB_PASSWORD = 'admin'
DB_NAME = 'postgres'
DRIVER = 'postgres+psycopg2'


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'{DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@' \
        f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + '/photo_storage'
