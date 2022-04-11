from requests import get

def get_soundcloud_id(text):
    try:
        soundcloud_url =  list(filter(lambda x: "https://soundcloud.com/" in x, text.split()))[0]
        params = {
            "format": 'json',
            "url": soundcloud_url,
            "maxwidth": "548.949"
        }
        soundcloud_data = get("https://soundcloud.com/oembed/", params=params).json()
    except IndexError:
        return None, None
    return soundcloud_data, soundcloud_url
