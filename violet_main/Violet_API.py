import base64
from datetime import datetime
import io
import os
import subprocess
import flask
from pytest import param
from requests import get
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from violet_main.api.music_and_videos_api import get_soundcloud_id
from violet_main.api.music_and_videos_api import get_yandexmusic_id
from violet_main.api.music_and_videos_api import get_youtube_id
from violet_main.data import db_session
from violet_main.data.news import News
from violet_main.data.users import User
from violet_main.data.news_embed import NewsEmbed
from violet_main.api.music_and_videos_api import get_spotify_id

app_api = "XYGD6dX+$Zi1Tw2z"
api_route = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)

@api_route.route('/api/news', methods=['POST'])
def create_news():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["api_key", 'content', 'user_id', 'images', 'is_private']):
        return jsonify({'error': 'Bad request'})
    elif db_sess.query(User).filter(User.bot_id == request.json['api_key']).first() is not None or\
        request.json['api_key'] != app_api:
        return jsonify({'error': 'wrong api key'})
    news_text = request.json['content']
    news = News(
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private'],
        images=request.json['images'],
    )
    embed = NewsEmbed()
    if "https://open.spotify.com/" in news_text:
        has, out = get_spotify_id(news_text)
        if has["track"]:
            embed.spotify_track = out["spotify_track"]
            news.embeds = True
        if has['playlist']:
            embed.spotify_playlist  = out["spotify_playlist"]
            news.embeds = True
        if has['album']:
            embed.spotify_album = out["spotify_album"]
            news.embeds = True
    if "https://youtu.be/" in news_text:
        has, out = get_youtube_id(news_text)
        if has["youtube_video"]:
            embed.youtube_video = out["youtube_video"]
            news.embeds = True
    if "https://soundcloud.com/" in news_text:
        soundcloud_data, soundcloud_url = get_soundcloud_id(news_text)
        if soundcloud_data != None:
            news.embeds = True
            embed.soundcloud_link = soundcloud_url
            embed.soundcloud_song_author = soundcloud_data["author_name"]
            embed.soundcloud_song_title = soundcloud_data["title"]
            embed.soundcloud_song_img = soundcloud_data["thumbnail_url"]
            embed.soundcloud_song_author_link = soundcloud_data["author_url"]
            embed.soundcloud_html = soundcloud_data["html"]
    if "https://music.yandex.ru/" in news_text:
        yandex_music_song_src, has = get_yandexmusic_id(news_text)
        if yandex_music_song_src != None:
            if has["track"]:
                embed.yandex_music_track = True
            if has['playlist']:
                embed.yandex_music_playlist  = True
            if has['album']:
                embed.yandex_music_album = True
            news.embeds = True
            embed.yandex_music_song_src = yandex_music_song_src
    db_sess.add(news)
    db_sess.commit()
    db_sess.add(embed)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@api_route.route('/api/images', methods=['GET', 'POST'])
def post_image():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["api_key", 'image_name', 'image_bin']):
        return jsonify({'error': 'Bad request'})
    elif db_sess.query(User).filter(User.bot_id == request.json['api_key']).first() is not None or\
        request.json['api_key'] != app_api:
        return jsonify({'error': 'wrong api key'})
    filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + request.json['image_name']
    filename = secure_filename(filename).split(".")
    filename_raw = generate_password_hash(filename[0])
    filename = filename_raw + "." + filename[1]
    filename = secure_filename(filename)
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
        "static/files", filename), "wb") as file:
        file.write(base64.b64decode(request.json['image_bin'].encode('utf-8')))
    command = "npx @squoosh/cli --webp auto " + "violet_main/static/files/" +\
                 filename + " --output-dir violet_main/static/files/webp"
    subprocess.call(command, shell = True)
    os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
        "static/files", filename))
    filename = filename_raw + ".webp"
    filename = secure_filename(filename)
    filename = "webp/" + filename
    return jsonify(
        {
            'file_name': filename
        }
    )

@api_route.route('/api/news', methods=['DELETE'])
def delete_news():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["api_key", 'id']):
        return jsonify({'error': 'Bad request'})
    elif db_sess.query(User).filter(User.bot_id == request.json['api_key']).first() is not None or\
        request.json['api_key'] != app_api:
        return jsonify({'error': 'wrong api key'})
    news = db_sess.query(News).get(request.json['id'])
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})