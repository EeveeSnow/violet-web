"""
Routes and views for the flask application.
"""

from datetime import datetime
import os
import hashlib
import subprocess
from types import NoneType
from flask import Flask, make_response, redirect, render_template, session
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from violet_main import app
from violet_main.data.news import News
from violet_main.data.users import User
from violet_main.data import db_session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from violet_main.forms.NewsForm import NewsForm
from violet_main.forms.PhotoForm import UploadForm
from violet_main.forms.RegisterForm import RegisterForm
from violet_main.forms.LoginForm import LoginForm


db_session.global_init("violet_main/db/data.db")
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_PATH = "server/images"

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
@app.route('/news')
def home():
    """Renders the home page."""
    param = {}
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
    else:
        param["user"] = "Войдите в аккаунт"
        param["image"] = None
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True) 
    return render_template(
        'index.html', param=param, news=news
        )

@app.route('/user_id:<int:user_id>')
def profile(user_id):
    param = {}
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        param["now_id"] = current_user.id
    else:
        param["user"] = "Войдите в аккаунт"
        param["image"] = None
        param["now_id"] = ""
    param["id"] = user_id
    db_sess = db_session.create_session()
    if param["now_id"] == param["id"]:
        news = db_sess.query(News).filter(News.user_id == user_id) 
    else:
        news = db_sess.query(News).filter(News.user_id == user_id).filter(News.is_private != True) 
    profile_inf = db_sess.query(User).filter(User.id == user_id)
    exist = profile_inf.first() is not None
    return render_template('profile.html', param=param, news=news, profile=profile_inf, profile_exs=exist)

@app.route('/image:<path:image_uri>:<int:code>')
def image(image_uri, code):
    return render_template('image.html', image_uri=image_uri)


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

#ERRORS PAGES
@app.errorhandler(418)
@app.route('/teapot')
def teapot():
    """Renders the teapot error page."""
    return render_template(
        'errors/teapot.html',
        title='Teapot'
    )

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html', title="404"), 404

@app.errorhandler(500)
def error500(e):
    """Renders the 500 error page."""
    return render_template(
        'errors/500.html',
        title='500'
    )

@app.route("/main")
def main():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords not the same")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Whoops we already have some one with this name(")
        user = User(
            user=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong login or password",
                               form=form)
    return render_template('login.html', title='Autorisation', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/add_news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    form2 = UploadForm()
    filename = None
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        if form2.image.data != None:
            file = form2.image.data
            filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + file.filename
            filename = secure_filename(filename).split(".")
            filename_raw = generate_password_hash(filename[0])
            filename = filename_raw + "." + filename[1]
            filename = secure_filename(filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],filename))
            command = "npx @squoosh/cli --webp auto " + "violet_main/static/files/" +\
                 filename + " --output-dir violet_main/static/files/webp"
            print(command)
            subprocess.call(command, shell = True)
            filename = filename_raw + ".webp"
            filename = secure_filename(filename)
            filename = "webp/" + filename
            news.images = filename
        news_text = form.content.data
        news_text_parced = news_text.split()
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
                news_youtube_id = list(filter(lambda x: ".be/" in x, news_text_parced))[0].split(".be/")[1].split()[0]
                has_youtube = True
            except IndexError:
                has_youtube = False
            if has_youtube:
                news.youtube_video = news_youtube_id
        news.content = news_text
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', 
                           form=form, image_form=form2)