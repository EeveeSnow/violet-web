news_text = "Lisen my new track  on spotify! here is a link: https://youtu.be/Pnp_7IaqW74"
news_text_parced = news_text.split()
if "https://open.spotify.com/" in news_text:
    news_text_parced = news_text.split("https://open.spotify.com/")
    try:
        news_track_id = list(filter(lambda x: "track/" in x, news_text_parced))[0].split("track/")[1].split()[0]
        has_track = True
    except IndexError:
        has_track = False
    try:
        news_playlist_id = list(filter(lambda x: "playlist/" in x, news_text_parced))[0]\
            .split("playlist/")[1].split()[0].split("?")[0]
        has_playlist = True
    except IndexError:
        has_playlist = False
    if has_track:
        print(news_track_id)
    if has_playlist:
        print(news_playlist_id)
if "https://youtu.be/" in news_text:
    news_text_parced = news_text.split("https://youtu")
    youtube_id = list(filter(lambda x: ".be/" in x, news_text_parced))[0].split(".be/")[1].split()[0]
    has_youtube = True
    print(youtube_id)

