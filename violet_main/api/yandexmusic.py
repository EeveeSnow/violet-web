from requests import get

def get_yandexmusic_id(text):
    try:
        yandexmusic_url = list(filter(lambda x: "https://music.yandex.ru/" in x, text.split()))[0]
        yandexmusic_song_album_id = yandexmusic_url.split("/")[4]
        yandexmusic_song_id = yandexmusic_url.split("/")[6]
        yandex_music_song_src = yandexmusic_song_id + "/" + yandexmusic_song_album_id
    except IndexError:
        return None
    return yandex_music_song_src