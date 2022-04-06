import base64
from datetime import datetime
import io
import os
import subprocess
import flask
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from violet_main.data import db_session
from violet_main.data.news import News
from violet_main.data.users import User

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
    if "https://open.spotify.com/" in news_text:
        news_text_parced = news_text.split("https://open.spotify.com/")
        try:
            news_track_id = list(filter(lambda x: "track/" in x, news_text_parced))[0]\
                .split("track/")[1].split()[0].split("?")[0]
            has_track = True
        except IndexError:
            has_track = False
        try:
            news_playlist_id = list(filter(lambda x: "playlist/" in x, news_text_parced))[0]\
                .split("playlist/")[1].split()[0].split("?")[0]
            has_playlist = True
        except IndexError:
            has_playlist = False
        try:
            news_album_id = list(filter(lambda x: "album/" in x, news_text_parced))[0]\
                .split("album/")[1].split()[0].split("?")[0]
            has_album = True
        except IndexError:
            has_album = False
        if has_track:
            news.spotify_track = news_track_id
        if has_playlist:
            news.spotify_playlist = news_playlist_id
        if has_album:
            news.spotify_album = news_album_id
    if "https://youtu.be/" in news_text:
        news_text_parced = news_text.split("https://youtu")
        try:
            news_youtube_id = list(
                filter(lambda x: ".be/" in x, news_text_parced))[0].split(".be/")[1].split()[0]
            has_youtube = True
        except IndexError:
            has_youtube = False
        if has_youtube:
            news.youtube_video = news_youtube_id
    db_sess.add(news)
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
    