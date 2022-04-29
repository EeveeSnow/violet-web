import sqlalchemy
from .db_session_cm import SqlAlchemyBase

class MessengerEmbed(SqlAlchemyBase):
    __tablename__ = 'messenger_embed'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    from_to = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    # SOUNDCLOUD

    soundcloud_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_author = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_song_author_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    soundcloud_html = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # YANDEX_MUSIC

    yandex_music_song_src = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    yandex_music_track = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    yandex_music_playlist = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    yandex_music_album = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    # SPOTIFY

    spotify_track = sqlalchemy.Column(sqlalchemy.String, nullable=True) 

    spotify_playlist = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    spotify_album = sqlalchemy.Column(sqlalchemy.String, nullable=True) 

    # YOUTUBE

    youtube_video = sqlalchemy.Column(sqlalchemy.String, nullable=True)