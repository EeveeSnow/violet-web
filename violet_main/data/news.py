import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
                                     
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))

    spotify_track = sqlalchemy.Column(sqlalchemy.String, nullable=True) 

    spotify_playlist = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    spotify_album = sqlalchemy.Column(sqlalchemy.String, nullable=True) 

    youtube_video = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    embeds = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = orm.relation('User')
