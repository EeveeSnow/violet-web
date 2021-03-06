"""
Routes and views for the flask application.
"""

import hashlib
import os
import random
import string
import subprocess
from datetime import datetime

from flask import redirect, render_template
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from requests import delete, post
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from violet_main import Violet_API
from violet_main.data import db_session, db_session_cm
from violet_main.data.chats import Chats
from violet_main.data.friends import Friends
from violet_main.data.messenger import Messenger
from violet_main.data.messenger_embed import MessengerEmbed
from violet_main.data.news import News
from violet_main.data.news_comments import NewsComments
from violet_main.data.news_embed import NewsEmbed
from violet_main.data.settings import Settings
from violet_main.data.users import User
from violet_main.forms.LoginForm import LoginForm
from violet_main.forms.MessageForm import MessageForm
from violet_main.forms.NewsForm import NewsForm
from violet_main.forms.PhotoForm import UploadForm, UploadForm2
from violet_main.forms.RegisterForm import RegisterForm
from violet_main.forms.SearchForm import SearchForm
from violet_main.wsgi import app

db_session.global_init("violet_main/db/data.db")
db_session_cm.global_init("violet_main/db/messenger.db")
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
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
    else:
        param["user"] = "?????????????? ?? ??????????????"
        param["image"] = None
        settings = None
    embeds = db_sess.query(NewsEmbed)
    news = db_sess.query(News).filter(
        News.is_private != True).order_by(News.created_date.desc())
    return render_template(
        'index.html', title="??????????????", param=param, news=news, embeds=embeds, settings=settings
    )


@app.route('/user_id:<int:user_id>')
def profile(user_id):
    param = {}
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        param["now_id"] = current_user.id
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
    else:
        param["user"] = "?????????????? ?? ??????????????"
        param["image"] = None
        param["now_id"] = ""
        settings = None
    param["id"] = user_id
    if param["now_id"] == param["id"]:
        news = db_sess.query(News).filter(
            News.user_id == user_id).order_by(News.created_date.desc())
    else:
        news = db_sess.query(News).filter(News.user_id == user_id)\
            .filter(News.is_private != True).order_by(News.created_date.desc())
    profile_inf = db_sess.query(User).filter(User.id == user_id)
    friends_tb = db_sess.query(Friends).filter(Friends.id == user_id)
    embeds = db_sess.query(NewsEmbed)
    exist = profile_inf.first() is not None
    return render_template('profile.html', title="??????????????", param=param, news=news,
                           profile=profile_inf, profile_exs=exist, embeds=embeds, settings=settings, friends_tb=friends_tb)


@app.route('/friends:<int:user_id>', methods=['GET', 'POST'])
def friends(user_id):
    form = SearchForm()
    param = {}
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        param["now_id"] = current_user.id
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
    else:
        param["user"] = "?????????????? ?? ??????????????"
        param["image"] = None
        param["now_id"] = ""
        settings = None
    param["id"] = user_id
    profile_inf = db_sess.query(User).filter(User.id == user_id)
    user = db_sess.query(User)
    friends = db_sess.query(Friends).filter(Friends.id == user_id)
    exist = profile_inf.first() is not None
    if form.validate_on_submit():
        return redirect(f"/search:{form.search.data}")
    return render_template('friends.html', title="????????????", param=param, user=user, profile_exs=exist,
                           settings=settings, friends=friends, profile_inf=profile_inf, form=form, users_s=None)


@app.route('/search:<string:user>', methods=['GET', 'POST'])
def search(user):
    form = SearchForm()
    param = {}
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        param["now_id"] = current_user.id
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
    else:
        param["user"] = "?????????????? ?? ??????????????"
        param["image"] = None
        param["now_id"] = ""
        settings = None
    users_s = db_sess.query(User).filter(User.user.like(f'%{user}%'))
    if form.validate_on_submit():
        return redirect(f"/search:{form.search.data}")
    return render_template('friends.html', title="??????????", param=param, user=None, friends=None,
                           settings=settings, form=form, users_s=users_s)


@app.route('/image:<path:image_uri>:<int:code>')
def image(image_uri, code):
    return render_template('image.html', title="??????????????????????", image_uri=image_uri)


@app.route('/news:<int:news_id>')
def news_extra(news_id):
    param = {}
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
    else:
        param["user"] = "?????????????? ?? ??????????????"
        param["image"] = None
        settings = None
    embeds = db_sess.query(NewsEmbed).filter(NewsEmbed.id == news_id)
    # comments = db_sess.query(NewsComments).filter(NewsComments.news_id == news_id)
    news = db_sess.query(News).filter(
        News.is_private != True).filter(News.id == news_id)
    return render_template(
        'news_page.html', title="??????????????", param=param, news=news, embeds=embeds, settings=settings
    )


@app.route('/delete_news:<int:news_id>')
def news_deletion(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == news_id)[0]
    server = "https://violet-web.herokuapp.com"
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


@app.route('/settings')
@login_required
def settings():
    return render_template("settings.html")


@app.route('/settings/change_theme')
@login_required
def change_theme_page():
    return render_template("settings_theme.html")


@app.route('/settings/change_theme/change_to:<string:theme_type>')
@login_required
def change_theme(theme_type):
    db_sess = db_session.create_session()
    settings = db_sess.query(Settings).filter(
        Settings.id == current_user.id).first()
    settings.theme = theme_type
    db_sess.commit()
    return redirect('/')


@app.route('/add_to_friends:<int:user_id>')
@login_required
def add_to_friends(user_id):
    if current_user.id != user_id:
        db_sess = db_session.create_session()
        other_user = db_sess.query(Friends).filter(
            Friends.id == user_id).first()
        curent_user = db_sess.query(Friends).filter(
            Friends.id == current_user.id).first()
        if curent_user.subscribers != None:
            if str(user_id) in curent_user.subscribers:
                other = str(other_user.subscribe_to).split()
                curent = str(curent_user.subscribers).split()
                curent.remove(str(user_id))
                other.remove(str(current_user.id))
                curent = " ".join(curent)
                other = " ".join(other)
                other_user.subscribe_to = other
                curent_user.subscribers = curent
                if other_user.friends != None:
                    other_user.friends = other_user.friends + \
                        " " + str(current_user.id)
                else:
                    other_user.friends = str(current_user.id)
                if curent_user.friends != None:
                    curent_user.friends = curent_user.friends + \
                        " " + str(user_id)
                else:
                    curent_user.friends = str(user_id)
            else:
                if other_user.subscribers != None:
                    other_user.subscribers = other_user.subscribers + \
                        " " + str(current_user.id)
                else:
                    other_user.subscribers = str(current_user.id)
                if curent_user.subscribe_to != None:
                    curent_user.subscribe_to = curent_user.subscribe_to + \
                        " " + str(user_id)
                else:
                    curent_user.subscribe_to = str(user_id)
        else:
            if other_user.subscribers != None:
                other_user.subscribers = other_user.subscribers + \
                    " " + str(current_user.id)
            else:
                other_user.subscribers = str(current_user.id)
            if curent_user.subscribe_to != None:
                curent_user.subscribe_to = curent_user.subscribe_to + \
                    " " + str(user_id)
            else:
                curent_user.subscribe_to = str(user_id)
        db_sess.commit()
    return redirect(f'/user_id:{user_id}')


@app.route('/delete_from_friends:<int:user_id>')
@login_required
def delete_from_friends(user_id):
    if current_user.id != user_id:
        db_sess = db_session.create_session()
        other_user = db_sess.query(Friends).filter(
            Friends.id == user_id).first()
        curent_user = db_sess.query(Friends).filter(
            Friends.id == current_user.id).first()
        other = str(other_user.friends).split()
        curent = str(curent_user.friends).split()
        curent.remove(str(user_id))
        other.remove(str(current_user.id))
        curent = " ".join(curent)
        other = " ".join(other)
        other_user.friends = other
        curent_user.friends = curent
        if curent_user.subscribers != None:
            curent_user.subscribers = curent_user.subscribers + \
                " " + str(user_id)
        else:
            curent_user.subscribers = str(user_id)
        if other_user.subscribe_to != None:
            other_user.subscribe_to = curent_user.subscribe_to + \
                " " + str(current_user.id)
        else:
            other_user.subscribe_to = str(current_user.id)
        db_sess.commit()
    return redirect(f'/user_id:{user_id}')


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

# ERRORS PAGES


@app.errorhandler(418)
@app.route('/teapot')
def teapot():
    """Renders the teapot error page."""
    return render_template(
        'errors/teapot.html',
        title='Teapot'
    )


@app.errorhandler(401)
def not_login(e):
    return redirect("/register")


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
        settings = Settings(
        )
        friends = Friends()
        db_sess_cm = db_session_cm.create_session()
        ch = Chats()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.add(settings)
        db_sess.add(friends)
        db_sess_cm.add(ch)
        db_sess.commit()
        db_sess_cm.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
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
                                   app.config['UPLOAD_FOLDER'], filename))
            command = "npx @squoosh/cli --webp auto " + "violet_main/static/files/" +\
                filename + " --output-dir violet_main/static/files/webp"
            subprocess.call(command, shell=True)
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config['UPLOAD_FOLDER'], filename))
            filename = filename_raw + ".webp"
            filename = secure_filename(filename)
            filename = "webp/" + filename
        server = "https://violet-web.herokuapp.com"
        print(post(f'{server}/api/news',
                   json={'api_key': "XYGD6dX+$Zi1Tw2z",
                         'content': form.content.data,
                         'user_id': current_user.id,
                         'images': filename,
                         'is_private': form.is_private.data}).json())
        return redirect('/')
    return render_template('news.html', title="?????????????????? ??????????????",
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
        settings = Settings(
        )
        friends = Friends()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.add(settings)
        db_sess.add(friends)
        db_sess.commit()
        return redirect('/')
    return render_template('api.html', title='Registration', form=form)


@app.route('/change_photo',  methods=['GET', 'POST'])
@login_required
def change_photo():
    form = UploadForm2()
    filename = None
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        file = form.image.data
        filename = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + file.filename
        filename = secure_filename(filename).split(".")
        filename_raw = generate_password_hash(filename[0])
        filename = filename_raw + "." + filename[1]
        filename = secure_filename(filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], filename))
        command = "npx @squoosh/cli --webp auto " + "violet_main/static/files/" +\
            filename + " --output-dir violet_main/static/files/webp"
        subprocess.call(command, shell=True)
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], filename))
        filename = filename_raw + ".webp"
        filename = secure_filename(filename)
        filename = "webp/" + filename
        profile = db_sess.query(User).filter(
            User.id == current_user.id).first()
        profile.image = filename
        db_sess.commit()
        return redirect('#')
    return render_template('image_upload.html', title="???????????????? ??????????????????????", image_form=form)


@app.route('/bot_info')
@login_required
def bot_info():
    db_sess = db_session.create_session()
    profile = db_sess.query(User).filter(User.id == current_user.id).first()
    return render_template('bot-info.html', item=profile)


@app.route('/start_chat:<int:user_id>')  # ?????????????? ???????????? ?? ?????????? ??????????
@login_required
def start_chat(user_id):
    if current_user.id != user_id:
        db_sess_cm = db_session_cm.create_session()
        other_user = db_sess_cm.query(Chats).filter(
            Chats.id == user_id).first()
        curent_user = db_sess_cm.query(Chats).filter(
            Chats.id == current_user.id).first()
        if curent_user.chats == None or curent_user.chats == "":
            if other_user.chats != None:
                other_user.chats = other_user.chats + \
                    " " + str(current_user.id)
            else:
                other_user.chats = str(current_user.id)
            if curent_user.chats != None:
                curent_user.chats = curent_user.chats + " " + str(user_id)
            else:
                curent_user.chats = str(user_id)
        elif str(user_id) not in curent_user.chats:
            if other_user.chats != None:
                other_user.chats = other_user.chats + \
                    " " + str(current_user.id)
            else:
                other_user.chats = str(current_user.id)
            if curent_user.chats != None:
                curent_user.chats = curent_user.chats + " " + str(user_id)
            else:
                curent_user.chats = str(user_id)
        else:
            # ?????????? ?????? ???????? > ???????????????????????????? ???? ????????
            return redirect(f'/messenger:{user_id}')
        db_sess_cm.commit()
        return redirect(f'/messenger:{user_id}')
    return redirect(f'/user_id:{user_id}')


@app.route('/chats')
@login_required
def chats():
    param = {}
    db_sess = db_session.create_session()
    db_sess_cm = db_session_cm.create_session()
    if current_user.is_authenticated:
        param["user"] = current_user.user
        param["image"] = current_user.image
        param["now_id"] = current_user.id
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
    else:
        param["user"] = "?????????????? ?? ??????????????"
        param["image"] = None
        param["now_id"] = ""
        settings = None
    user = db_sess.query(User)
    chats = db_sess_cm.query(Chats).filter(Chats.id == current_user.id).first()
    return render_template('chats.html', title="????????????????????", param=param, settings=settings, chats=chats, user=user)


# ???????????????????? ?? ??????-????. ?????????????? ?????????????? ?? ??????
@app.route('/messenger:<int:user_id>', methods=['GET', 'POST'])
@login_required
def messenger(user_id):
    if current_user.id != user_id:
        param = {}
        form = MessageForm()
        db_sess = db_session.create_session()
        db_sess_cm = db_session_cm.create_session()
        param["user"] = current_user.user
        param["image"] = current_user.image
        param["now_id"] = current_user.id
        settings = db_sess.query(Settings).filter(
            Settings.id == current_user.id).first()
        other_user = db_sess.query(User).filter(User.id == user_id).first()
        chat_name = 'to'.join(sorted([str(user_id), str(current_user.id)]))
        messages = db_sess_cm.query(Messenger).filter(
            Messenger.from_to == chat_name)
        embeds = db_sess_cm.query(MessengerEmbed).filter(
            MessengerEmbed.from_to == chat_name)
        if form.validate_on_submit():
            server = "https://violet-web.herokuapp.com"
            print(post(f'{server}/api/message',
                   json={'api_key': "XYGD6dX+$Zi1Tw2z",
                         'content': form.content.data,
                         'user_id': current_user.id,
                         "chat_name": chat_name}).json())   
        return render_template('messages.html', title="??????", param=param, messages=messages,
                               user=other_user, settings=settings, form=form, embeds=embeds)
    # ???????? ?????????? ???????????? ????????, ???? ?????????????????? ???????????? ???? ?????????????? ???? ?????????? ???????????????? ?????????? ??????????
    return redirect(f'/chats:{current_user.id}')
