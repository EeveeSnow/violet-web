"""
Routes and views for the flask application.
"""

import hashlib
import random
import string
import os
import subprocess
from datetime import datetime

from flask import redirect, render_template
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from requests import post, delete
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from violet_main import Violet_API, app
from violet_main.data import db_session
from violet_main.data.news import News
from violet_main.data.news_comments import NewsComments
from violet_main.data.news_embed import NewsEmbed
from violet_main.data.users import User
from violet_main.forms.LoginForm import LoginForm
from violet_main.forms.NewsForm import NewsForm
from violet_main.forms.PhotoForm import UploadForm
from violet_main.forms.RegisterForm import RegisterForm


db_session.global_init("violet_main/db/data.db")
login_manager = LoginManager()
login_manager.init_app(app)
UPLOAD_PATH = "server/images"
app.register_blueprint(Violet_API.api_route)


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
    embeds = db_sess.query(NewsEmbed)
    news = db_sess.query(News).filter(News.is_private != True).order_by(News.created_date.desc())
    return render_template(
        'index.html', param=param, news=news, embeds=embeds
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

@app.route('/news:<int:news_id>')
def news_extra(news_id):
    param = {}
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
    else:
        param["user"] = "Войдите в аккаунт"
        param["image"] = None
    db_sess = db_session.create_session()
    embeds = db_sess.query(NewsEmbed).filter(NewsEmbed.id == news_id)
    # comments = db_sess.query(NewsComments).filter(NewsComments.news_id == news_id)
    news = db_sess.query(News).filter(News.is_private != True).filter(News.id == news_id)
    return render_template(
        'news_page.html', param=param, news=news, embeds=embeds
        )

@app.route('/delete_news:<int:news_id>')
def news_deletion(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == news_id)[0]
    server = "http://localhost:5000"
    try:
        if news.user.id == current_user.id:
           print(delete(f'{server}/api/news',
           json={'api_key': "XYGD6dX+$Zi1Tw2z",
                 'id': news.id}).json())
    except:
        return redirect('/')
    return redirect('/')


@app.route('/for_devs')
def dev():
    return render_template("dev_page_layout.html")


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
            subprocess.call(command, shell = True)
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],filename))
            filename = filename_raw + ".webp"
            filename = secure_filename(filename)
            filename = "webp/" + filename
        server = "http://localhost:5000"
        print(post(f'{server}/api/news',
           json={'api_key': "XYGD6dX+$Zi1Tw2z",
                 'content': form.content.data,
                 'user_id': current_user.id,
                 'images': filename,
                 'is_private': form.is_private.data}).json())
        return redirect('/')
    return render_template('news.html', 
                           form=form, image_form=form2)

@app.route('/api-bot-register', methods=['GET', 'POST'])
def bot_register():
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
                                   message="Whoops we already have some one with this mail(")
        key_search = True
        while key_search:
            letters_and_digits = string.ascii_letters + string.digits
            rand_string = ''.join(random.sample(letters_and_digits, 16))
            key = hashlib.sha1(rand_string.encode('utf-8')).hexdigest()
            if db_sess.query(User).filter(User.bot_id == key).first() is None:
                key_search = False
        user = User(
            user=form.name.data,
            email=form.email.data,
            is_bot=True,
            bot_id=key
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('api.html', title='Registration', form=form)