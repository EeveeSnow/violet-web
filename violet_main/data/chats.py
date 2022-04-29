import sqlalchemy
from .db_session_cm import SqlAlchemyBase


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
        primary_key=True, autoincrement=True)

    chats = sqlalchemy.Column(sqlalchemy.String, nullable=True)