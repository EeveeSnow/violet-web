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