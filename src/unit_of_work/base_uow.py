class BaseUOW:
    def __init__(self, db_session):
        self.db_session = db_session

    def commit(self):
        self.db_session.commit()

    def rollback(self):
        self.db_session.rollback()
