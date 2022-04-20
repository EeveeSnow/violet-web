from requests import get


def get_yandexmusic_id(text):
    has = {}
    has_track = False
    has_playlist = False
    has_album = False
    try:
        yandexmusic_url = list(
            filter(lambda x: "https://music.yandex.ru/" in x, text.split()))[0]
        if "playlists" in yandexmusic_url:
            try:
                yandex_music_song_src = yandexmusic_url.split("/")[6]
                has_playlist = True
            except IndexError:
                has_playlist = False
        if "track" in yandexmusic_url and "album" in yandexmusic_url:
            try:
                yandexmusic_song_album_id = yandexmusic_url.split("/")[4]
                yandexmusic_song_id = yandexmusic_url.split("/")[6]
                has_track = True
                yandex_music_song_src = yandexmusic_song_id + "/" + yandexmusic_song_album_id
            except IndexError:
                has_track = False
        elif "album" in yandexmusic_url:
            try:
                yandex_music_song_src = yandexmusic_url.split("/")[4]
                has_album = True
            except IndexError:
                has_album = False
    except IndexError:
        return None, None
    has["track"] = has_track
    has["playlist"] = has_playlist
    has["album"] = has_album
    return yandex_music_song_src, has


def get_soundcloud_id(text):
    try:
        soundcloud_url = list(
            filter(lambda x: "https://soundcloud.com/" in x, text.split()))[0]
        params = {
            "format": 'json',
            "url": soundcloud_url,
            "maxwidth": "548.949"
        }
        soundcloud_data = get(
            "https://soundcloud.com/oembed/", params=params).json()
    except IndexError:
        return None, None
    return soundcloud_data, soundcloud_url


def get_spotify_id(text):
    text_parced = text.split("https://open.spot")
    out = {}
    has = {}
    try:
        track_id = list(filter(lambda x: "ify.com/track/" in x, text_parced))[0]\
            .split("track/")[1].split()[0].split("?")[0]
        has_track = True
    except IndexError:
        has_track = False
    try:
        playlist_id = list(filter(lambda x: "ify.com/playlist/" in x, text_parced))[0]\
            .split("playlist/")[1].split()[0].split("?")[0]
        has_playlist = True
    except IndexError:
        has_playlist = False
    try:
        album_id = list(filter(lambda x: "ify.com/album/" in x, text_parced))[0]\
            .split("album/")[1].split()[0].split("?")[0]
        has_album = True
    except IndexError:
        has_album = False
    if has_track:
        out["spotify_track"] = track_id
    if has_playlist:
        out["spotify_playlist"] = playlist_id
    if has_album:
        out["spotify_album"] = album_id
    has["track"] = has_track
    has["playlist"] = has_playlist
    has["album"] = has_album
    return has, out


def get_youtube_id(text):
    text_parced = text.split("https://youtu")
    out = {}
    has = {}
    try:
        youtube_id = list(
            filter(lambda x: ".be/" in x, text_parced))[0].split(".be/")[1].split()[0]
        has_youtube = True
    except IndexError:
        has_youtube = False
    if has_youtube:
        out["youtube_video"] = youtube_id
    has["youtube_video"] = has_youtube
    return has, out
