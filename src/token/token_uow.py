from src.repositories.sqlalchemy_uow import SqlAlchemyUnitOfWork


class TokenUnitOfWork(SqlAlchemyUnitOfWork):
    #TODO check_login_what_is
    def __init__(self, db_session):
        super().__init__(db_session)
        self.db_session = db_session

