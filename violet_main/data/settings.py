import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

class Settings(SqlAlchemyBase):
    __tablename__ = 'settings'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    theme = sqlalchemy.Column(sqlalchemy.String, default="Dark")

    date_form = sqlalchemy.Column(sqlalchemy.String, default="AM/PM")
 

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"), autoincrement=True)


    user = orm.relation('User')