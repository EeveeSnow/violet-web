import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class NewsEmbed(SqlAlchemyBase):
    __tablename__ = 'news_embed'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    # SOUNDCLOUD

    soundcloud_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_author = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_author_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_html = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # YANDEX_MUSIC

    yandex_music_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    yandex_music_song_src = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    yandex_music_song_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    yandex_music_song_author = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    yandex_music_song_author_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)




    



