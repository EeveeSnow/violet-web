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