import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News_Info(SqlAlchemyBase):
    __tablename__ = 'news_info'

    news_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("news.id"), primary_key=True)

    liked_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    news = orm.relation('News')