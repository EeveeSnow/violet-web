import sqlalchemy
from sqlalchemy import orm
import datetime

from .db_session import SqlAlchemyBase


class Friends(SqlAlchemyBase):
    __tablename__ = 'friends_table'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
        primary_key=True, autoincrement=True)

    friends = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    subscribers = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    subscribe_to = sqlalchemy.Column(sqlalchemy.String, nullable=True)
