import datetime
import sqlalchemy
from .db_session_cm import SqlAlchemyBase


class Messenger(SqlAlchemyBase):
    __tablename__ = 'messenger'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    from_to = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    sender = sqlalchemy.Column(sqlalchemy.Integer)
    embeds = sqlalchemy.Column(sqlalchemy.Boolean, default=False)