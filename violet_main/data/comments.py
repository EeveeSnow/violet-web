import sqlalchemy
from sqlalchemy import orm
import datetime

from .db_session import SqlAlchemyBase


class News_Info(SqlAlchemyBase):
    
    __tablename__ = 'news_comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
            primary_key=True, autoincrement=True)

    news_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("news.id"))

    comment_content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    comment_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')

    news = orm.relation('News')