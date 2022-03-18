import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Addons(SqlAlchemyBase):
    __tablename__ = 'addons'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    subscribed = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    liked = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    udate_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')
