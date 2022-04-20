import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class NewsComments(SqlAlchemyBase):

    __tablename__ = "news_comment"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    comment_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    
    news_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("news.id"))

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    yandex_music_song_src = sqlalchemy.Column(
        sqlalchemy.String, nullable=True)

    soundcloud_html = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    spotify_track = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    spotify_playlist = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    spotify_album = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    youtube_video = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    liked_by = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')

    news_table = orm.relation('News')
