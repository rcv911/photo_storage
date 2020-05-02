from app import db
import datetime


class Storage(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    system_name = db.Column(db.String(512), nullable=False)
    maker = db.Column(db.String(512), nullable=True)
    model = db.Column(db.String(512), nullable=True)
    size = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    uploaded = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, *args, **kwargs):
        super(Storage, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.id} - {self.name}'
