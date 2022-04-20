from requests import get

def get_yandexmusic_id(text):
    try:
        yandexmusic_url = list(filter(lambda x: "https://music.yandex.ru/" in x, text.split()))[0]
        try:
            yandexmusic_song_album_id = yandexmusic_url.split("/")[4]
            yandexmusic_album = True
        except IndexError:
            yandexmusic_album = False
        try:
            yandexmusic_song_id = yandexmusic_url.split("/")[6]
            yandexmusic_song = True
        except IndexError:
            yandexmusic_song = False
        if yandexmusic_album and yandexmusic_song:
            yandex_music_song_src = yandexmusic_song_id + "/" + yandexmusic_song_album_id
        elif yandexmusic_album:
            yandex_music_song_src = yandexmusic_song_album_id
        else:
            return None
    except IndexError:
        yandexmusic_album = False
        return None
    return yandex_music_song_src