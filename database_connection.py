

class Connection:

    def __init__(self, db):
        self.init_db(db)
        self.session = db.session

    @staticmethod
    def init_db(db):
        db.create_all()

    def close(self):
        self.session.close()
