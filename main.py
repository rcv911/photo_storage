import os
from app import app
import view
import models

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))
    storage = f'{basedir}/photo_storage'
    if not os.path.exists(storage):
        os.mkdir(storage)
    app.run()
